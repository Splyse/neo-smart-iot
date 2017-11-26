#!/usr/bin/env python3

"""
neo-pubsub.py

MIT License

Copyright 2017 Splyse Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

-----
About
-----

This script acts as a standalone neo-python node/MQTT pubsub server. It listens 
for Runtime.Notify events and publishes them to the MQTT queue to broadcast to 
subscribing clients such as IOT devices.

It is intended to run inside the ./contrib directory of a fully configured 
neo-python installation. (Due to limitations of LevelDB, it is not possible to 
run prompt.py while this script is running)

------------
Installation
------------

Additional libraries are needed over the default requirements of neo-python:

pip install hbmqtt paho-mqtt

"""

import os
import sys
import signal
import logging
import functools
import asyncio
import hbmqtt
import binascii
from hbmqtt.broker import Broker
from hbmqtt.mqtt.publish import PublishPacket
import paho.mqtt.publish as publish
from threading import Thread

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from contrib.smartcontract import SmartContract
from neo.Network.NodeLeader import NodeLeader
from twisted.internet import reactor, task
from neo.Core.Blockchain import Blockchain, Events
from neo.SmartContract.StateReader import StateReader
from neo.Implementations.Blockchains.LevelDB.LevelDBBlockchain import LevelDBBlockchain
from neo.Settings import settings

smart_contract = SmartContract("b3a14d99a3fb6646c78bf2f4e2f25a7964d2956a")

@smart_contract.on_notify
def sc_notify(event):
    if len(event.event_payload):
        #sender = event.event_payload[0].decode("utf-8")
        key = event.event_payload[1].decode("utf-8")
        pub = b'::'.join([binascii.unhexlify(item.decode()) for item in event.event_payload[2:]])
        print("**** NOTIFY: {}/{}/{}".format(event.contract_hash, key, pub))
        publish.single("Neo/{}/{}".format(event.contract_hash, key), payload=pub)

config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': '0.0.0.0:1883',
        },
    },
    'auth': {
        'allow-anonymous': True,
        'plugins': [
            'auth_anonymous',
        ]
    }
}


def do_quit():
    print('Shutting down.')
    Blockchain.Default().Dispose()
    reactor.stop()
    NodeLeader.Instance().Shutdown()
    sys.exit(0)


def signal_handler(signal, frame):
    do_quit()


def prefix_function(origfunction, prefunction):
    @functools.wraps(origfunction)
    @asyncio.coroutine
    def run(*args, **kwargs):
        prefunction(*args, **kwargs)
        return origfunction(*args, **kwargs)
    return run


# This functions as an ACL to ensure only localhost can publish to the queue
def acl_handle_publish(self, publish_packet: PublishPacket):
    peer = self.reader._reader._transport._extra['peername'][0]
    if peer == '127.0.0.1':
        pass
    else:
        print("PUBLISH {} from {} blocked!".format(publish_packet.data, peer))
        raise Exception("denied")
        return


@asyncio.coroutine
def broker_coro():
    broker = Broker(config)
    yield from broker.start()


def on_notify(ea):
    scripthash = ea.ScriptHash.ToString()
    if scripthash in watched_scripthashes:
        print("Got scripthash match for {}".format(scripthash))
        pub = b'' 
        key = b'' 
        if ea.State.IsArray:
            itemlist = ea.State.GetArray()
            sender = itemlist[0]._value
            key = itemlist[1]._value
            pub = b'::'.join([binascii.unhexlify(item._value.decode()) for item in itemlist[2:]])
        else:
            pub = b'{}'.format(ea.State._value)

        print("**** NOTIFY: {}/{}/{}".format(scripthash, key.decode(), pub))
        publish.single("Neo/{}/{}".format(scripthash, key.decode()), payload=pub)
    else:
        print("Scripthash {} not in watchlist, continuing...".format(scripthash))


def neo_loop():

    blockchain = LevelDBBlockchain(settings.LEVELDB_PATH)
    Blockchain.RegisterBlockchain(blockchain)
    print("PersistBlocks task starting")
    dbloop = task.LoopingCall(Blockchain.Default().PersistBlocks)
    dbloop.start(.01)

    print("Node task starting")
    NodeLeader.Instance().Start()
    
    print("Entering main reactor loop")
    reactor.run(installSignalHandlers=False)


def main():
    signal.signal(signal.SIGINT, signal_handler)

    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)

    print("Installing Runtime.Notify event handler")
    #StateReader.NotifyEvent.on_change += on_notify
    hbmqtt.mqtt.protocol.handler.ProtocolHandler.handle_publish = prefix_function(
        hbmqtt.mqtt.protocol.handler.ProtocolHandler.handle_publish, acl_handle_publish)

    print("Starting Neo thread")
    t = Thread(target=neo_loop)
    t.start()

    print("Starting MQTT broker task")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(broker_coro())
    loop.run_forever()


if __name__ == "__main__":
    main()
