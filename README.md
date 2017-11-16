# Neo Smart IoT

## Overview

Neo Smart IoT is a project contribution to the [Neo Smart Economy Network](http://neo.org) to enable control of [IoT](https://en.wikipedia.org/wiki/Internet_of_things) (Internet of Things) devices via Neo [smart contracts](http://docs.neo.org/en-us/sc/introduction.html).

To operate an IoT device, a contract may operate for free, take payment in the form of Neo or Gas, or hold Neo as a deposit that can be returned to the user when control is no longer needed.

At a high level, a smart contract is deployed to the Neo blockchain. This contract contains functionality that allows values to be sent to IoT devices to control them. I.e., a payment could be sent to control a device that opens a lock, plays a song on a jukebox, or dispenses an item from a vending machine. The possibilities are endless.


## Components

The Neo Smart IoT system consists of four components:

* Node.js web frontend

  This part allows a normal user to see devices available for control by the smart contract.
  The web frontend uses a Chrome extension called [NeoLink](https://github.com/CityOfZion/NeoLink) to authorize transactions.

* neo-pubsub.py

  Python Neo blockchain transaction monitor and MQTT queue

* elcaro-contract.py

  This is the Neo smart contract on the blockchain that stores devices and their fees, if any, to operate.


* IoT device firmware

  This is the code that operates the IoT device.


## Video Demonstration

Check out a video demonstration of the complete system over at the
[Splyse, Inc. YouTube channel](https://www.youtube.com/watch?v=GEc8gKIznYY).

  ## Run the Demo

  1. Go to https://github.com/CityOfZion/NeoLink and follow the instructions to setup NeoLink.

  2. Ensure that a wallet is open in NeoLink.

  3. Go to https://iot.splyse.tech

  4. Login with:

    email: neo@splyse.tech

    password: neo

  5. You should now be on the Devices page. Enter a color, in the form of ff00ff or similar, into the setting input field and press pay. If your wallet is open you should see a message in the web page telling you to open NeoLink and authorize a transaction.

  6. Open NeoLink and authorize the transaction. It will only cost .00025 gas on TestNet.
