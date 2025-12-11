from v import *

coinbase_trans = {"object":{"height":1,"outputs":[{"pubkey":pubkeys[0],"value":50000000000000}],"type":"transaction"},"type":"object"}

def gen_test_invalid_trans_block():
    description = "The Block references another block in txids"
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    coinbase_trans_1 = mkCoinbase(1, 2, 50000000000000)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans,0)],[transOut(3, 49999999999900)])
    full_signature(0, transfer_trans_2)
    mine(block_valid_1)
    block_invalid_2 = mkBlock(block_valid_1, [coinbase_trans_1, block_valid_1,transfer_trans_2], description)
    return {
            'description' : description,
            'expected': 'INVALID_FORMAT',
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, (block_valid_1,True), (block_invalid_2,False) ]
            }

def gen_test_invalid_block_trans():
    description = "A transaction references another block in inputs"
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    mine(block_valid_1)
    coinbase_trans_1 = mkCoinbase(1, 2, 50000000000000)
    transfer_trans_2 = mkTrans([transIn(0,block_valid_1,0)],[transOut(3, 49999999999900)])
    full_signature(0, transfer_trans_2)
    block_invalid_2 = mkBlock(block_valid_1, [coinbase_trans_1,transfer_trans_2], description)
    return {
            'description' : description,
            'expected': 'INVALID_FORMAT',
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, (block_valid_1,True), (block_invalid_2,False) ]
            }

def gen_test_tx_no_inputs():
    description = "A non-coinbase transaction has no inputs"
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    mine(block_valid_1)
    coinbase_trans_1 = mkCoinbase(1, 2, 50000000000000)
    transfer_trans_2 = mkTrans([],[transOut(3, 49999999999900)])
    full_signature(0, transfer_trans_2)
    block_invalid_2 = mkBlock(block_valid_1, [coinbase_trans_1,transfer_trans_2], description)
    return {
            'description' : description,
            'expected': 'INVALID_FORMAT',
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, (block_valid_1,True), (block_invalid_2,False) ]
            }

def gen_test_negative_output():
    description = "A non-coinbase transaction has a negative output"
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    mine(block_valid_1)
    coinbase_trans_1 = mkCoinbase(1, 2, 50000000000000)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans,0)],[transOut(3, -49999999999900)])
    full_signature(0, transfer_trans_2)
    block_invalid_2 = mkBlock(block_valid_1, [coinbase_trans_1,transfer_trans_2], description)
    return {
            'description' : description,
            'expected': 'INVALID_FORMAT',
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, (block_valid_1,True), (block_invalid_2,False) ]
            }
