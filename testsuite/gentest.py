#!/usr/bin/env python
# Copyright (C) 2025 Thomas Ogrisegg
# License: GPLv3

import hashlib
import binascii
from jcs import canonicalize
import json
import random
from cryptography.hazmat.primitives.asymmetric.ed25519 import *
from cryptography.hazmat.primitives.serialization import *
from v import *
import sys

def generate_keys():
    for i in range(0,9):
        privkeys.append(Ed25519PrivateKey.from_private_bytes(bytes("1234567890123456789012345678901"+str(i), "utf-8")))
        pubkeys.append(binascii.hexlify(privkeys[i].public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)).decode("ascii"))

def load_test(filename):
    file = open(filename)
    for line in file:
        for s in line.split():
            print(s)

def dump(testcase, filename):
    for i in testcase['objects']:
        obj = None
        if (isinstance(i, tuple)):
            if (isinstance(i[0], str) and i[0] == 'cmd'):
                continue
            obj = i[0]['object']
        else:
            obj = i['object']
        if (obj['type'] == 'block'):
            mine_block(obj)
    with open (filename, "w", encoding='utf-8') as file:
        file.write(json.dumps(testcase))

generate_keys()

if (len(sys.argv) == 1):
    print (f"usage: {sys.argv[0]} testcase [functions to generate]")
    exit (1)

i = __import__(sys.argv[1].removesuffix('.py'))
funcs = sys.argv[2:]
for x in dir(i):
    if (x.startswith("gen_test")):
        output = x[9:]
        if (len(funcs)>0):
            if (output not in funcs):
                continue
        print (f"Generating function {x}: " + x[9:])
        dump(getattr(i, x)(), f"{output}.json")
