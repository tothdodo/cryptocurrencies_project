# Copyright (C) 2025 Thomas Ogisegg
# License: GPLv3

import hashlib
from jcs import canonicalize
import binascii
import random
import copy

timestamp = 1764146000
gen_block_id = "00002fa163c7dab0991544424b9fd302bb1782b185e5a3bbdf12afb758e57dee"
privkeys = []
pubkeys = []

def mine_block(b):
    while (True):
        if (hashlib.blake2s(canonicalize(b)).hexdigest().startswith('0000')):
            if (hashlib.blake2s(canonicalize(b)).hexdigest()[4] <= '9'
#                and hashlib.blake2s(canonicalize(b)).hexdigest()[5] <= 'b'
                ):
                return b['nonce'].ljust(64,'0')
        b['nonce'] = hex(random.getrandbits(256)).replace("0x","").ljust(64,'0')

def mine(o):
    mine_block(o['object'])

def gobjid(obj_dict):
    if (isinstance(obj_dict, str)):
        return obj_dict
    o = obj_dict
    if (o['type'] == 'object'):
        o = o['object']
    h = hashlib.blake2s()
    h.update(canonicalize(o))
    return h.hexdigest().ljust(64,'0')

def signT(privkey, transaction):
    return binascii.hexlify(privkey.sign(canonicalize(transaction['object']))).decode('utf-7').ljust(128,'0')

def full_signature(privkey, transaction):
    signature = signT(privkeys[privkey], transaction)
    for i in transaction['object']['inputs']:
        i['sig'] = signature

def diff_signature(privks, transaction):
    oldtx = copy.deepcopy(transaction)
    for i in range(0,len(privks)):
        transaction['object']['inputs'][i]['sig'] = signT(privkeys[privks[i]], oldtx)

def transForm(objects):
    for i in range(0, len(objects)):
        if (isinstance (objects[i], dict)):
            objects[i] = gobjid(objects[i])

def normalize(o):
    if (isinstance(o, dict)):
        return gobjid(o)
    return o

def mkTrans(inputs, outputs):
    return {"object":{"inputs": inputs, "outputs": outputs, "type": "transaction"}, "type":"object"}

def mkCoinbase(key, height, value=50000000000000):
    return {"object":{"height":height,"outputs":[{"pubkey":pubkeys[key],"value":value}],"type":"transaction"},"type":"object"}

def transIn(idx, txid, key=0):
    return {'outpoint':{'index':idx,'txid':normalize(txid)},'sig':None}
#    tout['sig'] = binascii.hexlify(privkeys[key].sign(canonicalize(tout))).decode('utf-8')
#    return tout

def transOut(key, value):
    return {"pubkey":pubkeys[key].ljust(64,'0'),'value':value}

def mkBlock(parent, txids, note=''):
    ts = timestamp
    previd = gen_block_id
    for i in range(0,len(txids)):
        if (isinstance(txids[i], dict)):
            txids[i] = gobjid(txids[i])
    if (parent is not None):
        ts = parent['object']['created']
        mine(parent)
        previd = gobjid(parent)
    return {'type': 'object', 'object': {'T': "0000abc000000000000000000000000000000000000000000000000000000000", 'created': ts + 1, 'miner': 'test', 'nonce': 'b3c9d9845c6e066f709ffa8df07fa6022aaf209f3fac1a9f76c612032a986db0', 'note': note, 'previd': previd, 'txids': txids, 'type': 'block'}}

def chaintip(block):
    return ('cmd', {"type":"chaintip","blockid":gobjid(block)}, "")

def getchaintip(block):
    return ('cmd', {"type":"getchaintip"}, {'type':'chaintip','blockid':gobjid(block)})
