from v import *

coinbase_trans = {"object":{"height":1,"outputs":[{"pubkey":pubkeys[0],"value":50000000000000}],"type":"transaction"},"type":"object"}

def gen_test_invalid_target():
    block_invalid_target = mkBlock(None, [coinbase_trans], "This block has an invalid target")
    block_invalid_target['object']['T'] = "0000abc000000000000000000000000000000000000000000000000000000001"
#    block_invalid_target = {"type":"object","object":{"T":"0000abc000000000000000000000000000000000000000000000000000000001","created":timestamp,"miner":"test","nonce":"b3c9d9845c6e066f709ffa8df07fa6022aaf209f3fac1a9f76c612032a986db0","note":"This block has an invalid target","previd":gen_block_id,"txids":[coinbase_trans],"type":"block"}}

    return {
            'description' : 'Block with an invalid target',
            'expected': 'INVALID_FORMAT',
            'objects': [ coinbase_trans, (block_invalid_target,False) ]
            }

def gen_test_right_output():
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    coinbase_trans_1 = mkCoinbase(1, 2, 50000000000100)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans,0)],[transOut(3, 49999999999900)])
    full_signature(0, transfer_trans_2)
    mine(block_valid_1)
    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_1,transfer_trans_2], 'This block has two valid transactions')
    return {
            'description' : '2 Valid transactions',
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, (block_valid_1,True), (block_valid_2,True) ]
            }

def gen_test_invalid_height():
    description =  "Transaction with an invalid height"
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    coinbase_trans_1 = mkCoinbase(1, 1, 50000000000000)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans,0)],[transOut(3, 49999999999900)])
    full_signature(0, transfer_trans_2)
    mine(block_valid_1)
    block_invalid_2 = mkBlock(block_valid_1, [coinbase_trans_1,transfer_trans_2], description)
    return {
            'description' : description,
            'expected': 'INVALID_BLOCK_COINBASE',
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, (block_valid_1,True), (block_invalid_2,False) ]
            }

def gen_test_coinbase_2output():
    description = "Coinbase Transaction with too much output"
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    coinbase_trans_1 = mkCoinbase(1, 2, 50000000000101)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans,0)],[transOut(3, 49999999999900)])
    full_signature(0, transfer_trans_2)
    block_invalid_2 = mkBlock(block_valid_1, [coinbase_trans_1,transfer_trans_2], description)
    return {
            'description' : description,
            'expected': 'INVALID_BLOCK_COINBASE',
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, (block_valid_1,True), (block_invalid_2,False) ]
            }

def gen_test_coinbase_double():
    description = "Two Coinbase Transactions in one block"
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    coinbase_trans_1 = mkCoinbase(1, 2, 50000000000000)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans,0)],[transOut(3, 49999999999900)])
    full_signature(0, transfer_trans_2)
    block_invalid_2 = mkBlock(block_valid_1, [coinbase_trans_1,coinbase_trans_1,transfer_trans_2], description)
    return {
            'description' : description,
            'expected': 'INVALID_BLOCK_COINBASE',
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, (block_valid_1,True), (block_invalid_2,False) ]
            }

def gen_test_coinbase_wrong_pos():
    description = "The Coinbase Transactions is at the wrong position"
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    coinbase_trans_1 = mkCoinbase(1, 2, 50000000000000)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans,0)],[transOut(3, 49999999999900)])
    full_signature(0, transfer_trans_2)
    block_invalid_2 = mkBlock(block_valid_1, [transfer_trans_2,coinbase_trans_1], description)
    return {
            'description' : description,
            'expected': 'INVALID_BLOCK_COINBASE',
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, (block_valid_1,True), (block_invalid_2,False) ]
            }
