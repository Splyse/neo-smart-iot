"""
neo-pubsub.py

MIT License

Copyright 2017 Splyse Inc.
"""

from boa.blockchain.vm.System.ExecutionEngine import GetScriptContainer,GetExecutingScriptHash
from boa.blockchain.vm.Neo.Transaction import *
from boa.blockchain.vm.Neo.Runtime import GetTrigger,CheckWitness,Notify,Log
from boa.blockchain.vm.Neo.TriggerType import Application,Verification
from boa.blockchain.vm.Neo.Output import GetScriptHash,GetValue,GetAssetId
from boa.blockchain.vm.Neo.Storage import GetContext,Get,Put

from boa.code.builtins import concat,take

OWNER = b'\x8e\x5b\x17\x79\x3c\xa9\xf5\xd9\x13\x1d\x67\x4d\xfc\x00\x0f\x5a\x65\x58\xa4\x65'
GAS_ASSET_ID = b'\xe7\x2d\x28\x69\x79\xee\x6c\xb1\xb7\xe6\x5d\xfd\xdf\xb2\xe3\x84\x10\x0b\x8d\x14\x8e\x77\x58\xde\x42\xe4\x16\x8b\x71\x79\x2c\x60';
BADPREFIX='price/'

def Main(operation, args):

    trigger = GetTrigger()

    if trigger == Verification():
        return CheckWitness(OWNER)

    elif trigger == Application():
        context = GetContext()
        l = len(args)
        if l == 1:
            key = args[0]
        elif l == 2:
            key = args[0]
            value = args[1]
        else:
            Log("Bad invocation argument count")
            Log(l)
            return False

        if operation == 'getvalue':
            return Get(context, key)
  
        elif operation == 'putvalue':
            prefix = take(key, 6)
            if BADPREFIX == prefix:
                Log("Hacking attempt!")
                return False

            if CheckWitness(OWNER):
                Log("Owner found, bypassing payment")
                Put(context, key, value)
                return True
            else:
                # check if we got paid
                tx = GetScriptContainer()
                refs = tx.References
                if len(refs) < 1:
                    Log("No payment sent in transaction")
                    return False
                ref = refs[0]
                sentAsset = GetAssetId(ref)
                if sentAsset == GAS_ASSET_ID:
                    sender = GetScriptHash(ref)
                    receiver = GetExecutingScriptHash();
                    totalGasSent = 0
            
                    for output in tx.Outputs:
                        shash = GetScriptHash(output)
                        if shash == receiver:
                            totalGasSent = totalGasSent + output.Value

                    Log ("Total GAS sent:")
                    Log (totalGasSent)
                    pkey = concat('price/', key)
                    keyprice = Get(context, pkey)

                    if totalGasSent == keyprice:
                        Log("Price met, setting value and sending notification")
                        notification=[sender,key,value]
                        Notify(notification)
                        Put(context, key, value)
                        return True
                   
                    Log("Price not met!")
                    return False
            
            return False
        elif operation == 'getprice':
            key = concat('price/', key)
            return Get(context, key)

        elif operation == 'putprice':
            if CheckWitness(OWNER):
                key = concat('price/', key)
                Put(context, key, value)
                return True
            else:
                Log("Access denied")
                return False
        else:
            Log("Invalid operation")
            return False
    return False
