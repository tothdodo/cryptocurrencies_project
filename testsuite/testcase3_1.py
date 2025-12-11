from v import *

coinbase_trans = {"object":{"height":1,"outputs":[{"pubkey":pubkeys[0],"value":50000000000000}],"type":"transaction"},"type":"object"}

def gen_test_invalid_previd():
    block_invalid_previd = mkBlock(None, [coinbase_trans], "This block has an invalid previd ptr")
    block_invalid_previd['object']['previd'] = None

    return {
            'description' : 'Block with an invalid previd ptr',
            'expected': 'INVALID_GENESIS',
            'objects': [ coinbase_trans, (block_invalid_previd,False) ]
            }

def gen_test_unknown_object():
    block_unknown_obj = mkBlock(None, [coinbase_trans,"b3c9d9845c6e066f709ffa8df07fa6022aaf209f3fac1a9f76c612032a986db0"], "This block has an unknown txid")

    return {
            'description' : 'Coinbase block with unknown txid',
            'expected': 'UNFINDABLE_OBJECT',
            'objects': [ coinbase_trans, (block_unknown_obj,False) ]
            }

def gen_test_invalid_height():
    this_coinbase_trans = mkCoinbase(1, 2)
    block_invalid_height = mkBlock(None, [this_coinbase_trans], "This block has a tx with wrong height")
    return {
            'description' : 'Coinbase transaction has wrong height',
            'expected': 'INVALID_BLOCK_COINBASE',
            'objects': [ this_coinbase_trans, (block_invalid_height,False) ],
            }
