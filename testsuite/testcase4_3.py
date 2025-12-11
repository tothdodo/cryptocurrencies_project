from v import *

coinbase_trans = {"object":{"height":1,"outputs":[{"pubkey":pubkeys[0],"value":50000000000000}],"type":"transaction"},"type":"object"}

def gen_test_recursive_unknown_parent_invalid_tx1():
    description = "Unknown parent block, known transactions, invalid output (toplevel)"
    coinbase_trans_1 = mkCoinbase(0,3,50000000000000)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans_1)],[transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000)])
    full_signature (0, transfer_trans_2)
    transfer_trans_3 = mkTrans([transIn(0,transfer_trans_2),transIn(1,transfer_trans_2)],[transOut(1,25000000000001)])
    full_signature (0, transfer_trans_3)
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction, but unknown parent")
    block_valid_1['object']['previd'] = "00008d3ba4afc7e109612cb73acbdddac052c93025aa1f82942edabb7deb82a1"
    mine(block_valid_1)
    block_valid_2 = mkBlock (block_valid_1, [transfer_trans_2], "This block has a valid transaction")
    mine(block_valid_2)
    block_invalid_3 = mkBlock (block_valid_2, [transfer_trans_3], "This block has an invalid transaction")
    mine(block_invalid_3)
    return {
            'description' : description,
            'expected': 'INVALID_TX_CONSERVATION',
            'objects': [ coinbase_trans_1, transfer_trans_2, transfer_trans_3, block_valid_1, block_valid_2, (block_invalid_3,False)
            ]
    }

def gen_test_recursive_unknown_parent_invalid_tx2():
    description = "Unknown parent block, known transactions, invalid output (2nd level)"
    coinbase_trans_1 = mkCoinbase(0,3,50000000000000)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans_1)],[transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000001)])
    full_signature (0, transfer_trans_2)
    transfer_trans_3 = mkTrans([transIn(0,transfer_trans_2),transIn(1,transfer_trans_2)],[transOut(1,25000000000000)])
    full_signature (0, transfer_trans_3)
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction, but unknown parent")
    block_valid_1['object']['previd'] = "00008d3ba4afc7e109612cb73acbdddac052c93025aa1f82942edabb7deb82a1"
    mine(block_valid_1)
    block_invalid_2 = mkBlock (block_valid_1, [transfer_trans_2], "This block has an invalid transaction")
    mine(block_invalid_2)
    block_valid_3 = mkBlock (block_invalid_2, [transfer_trans_3], "This block has a valid transaction")
    mine(block_valid_3)
    return {
            'description' : description,
            'expected': 'INVALID_ANCESTRY',
            'objects': [ coinbase_trans_1, transfer_trans_2, transfer_trans_3, block_valid_1, block_invalid_2, (block_valid_3,False)
            ]
    }

# this test will only work on an empty DB
def gen_test_longest_chain():
    description = "Three chains, one is the longest, chaintipped"
    block_c1_valid_1 = mkBlock(None, [coinbase_trans], "Chain 1, Block 1")
    block_c2_valid_1 = mkBlock(None, [coinbase_trans], "Chain 2, Block 1")
    block_c3_valid_1 = mkBlock(None, [coinbase_trans], "Chain 3, Block 1")
    mine(block_c1_valid_1)
    mine(block_c2_valid_1)
    mine(block_c3_valid_1)
    coinbase_trans_2 = mkCoinbase(0,2,50000000000000)
    block_c1_valid_2 = mkBlock(block_c1_valid_1, [coinbase_trans_2], "Chain 1, Block 2")
    block_c2_valid_2 = mkBlock(block_c2_valid_1, [coinbase_trans_2], "Chain 1, Block 2")
    block_c3_valid_2 = mkBlock(block_c3_valid_1, [coinbase_trans_2], "Chain 1, Block 2")
    mine(block_c1_valid_2)
    mine(block_c2_valid_2)
    mine(block_c3_valid_2)
    coinbase_trans_3 = mkCoinbase(0,3,50000000000000)
    block_c1_valid_3 = mkBlock(block_c1_valid_2, [coinbase_trans_3], "Chain 1, Block 3")
    block_c2_valid_3 = mkBlock(block_c2_valid_2, [coinbase_trans_3], "Chain 2, Block 3")
    block_c3_valid_3 = mkBlock(block_c3_valid_2, [coinbase_trans_3], "Chain 3, Block 3")
    mine(block_c1_valid_3)
    mine(block_c2_valid_3)
    mine(block_c3_valid_3)
    coinbase_trans_4 = mkCoinbase(0,4,50000000000000)
    block_c1_valid_4 = mkBlock(block_c1_valid_3, [coinbase_trans_4], "Chain 1, Block 4")
    block_c2_valid_4 = mkBlock(block_c2_valid_3, [coinbase_trans_4], "Chain 2, Block 4")
    block_c3_valid_4 = mkBlock(block_c3_valid_3, [coinbase_trans_4], "Chain 3, Block 4")
    mine(block_c1_valid_4)
    mine(block_c2_valid_4)
    mine(block_c3_valid_4)
    coinbase_trans_5 = mkCoinbase(0,5,50000000000000)
    block_c1_valid_5 = mkBlock(block_c1_valid_4, [coinbase_trans_5], "Chain 1, Block 5")
    block_c2_valid_5 = mkBlock(block_c2_valid_4, [coinbase_trans_5], "Chain 2, Block 5")
    block_c3_valid_5 = mkBlock(block_c3_valid_4, [coinbase_trans_5], "Chain 3, Block 5")
    mine(block_c1_valid_5)
    mine(block_c2_valid_5)
    mine(block_c3_valid_5)
    return {
            'description': description,
            'objects': [ coinbase_trans, coinbase_trans_2, coinbase_trans_3, coinbase_trans_4, coinbase_trans_5, (block_c1_valid_1,True), block_c2_valid_1, block_c3_valid_1, block_c1_valid_2, (block_c2_valid_2,True), block_c3_valid_2, getchaintip(block_c2_valid_2), block_c1_valid_3, block_c2_valid_3, (block_c3_valid_3,True), getchaintip(block_c3_valid_3), (block_c1_valid_4,True), getchaintip(block_c1_valid_4), block_c2_valid_4, block_c3_valid_4, block_c1_valid_5, (block_c2_valid_5,True), block_c3_valid_5, getchaintip(block_c2_valid_5) ]
    }

# this test will only work on an empty DB
def gen_test_longest_chain_valid_no_parent():
    description = "Three chains, one is the longest, chaintipped, one has no parent (#2)"
    block_c1_valid_1 = mkBlock(None, [coinbase_trans], "Chain 1, Block 1 #")
    block_c2_valid_1 = mkBlock(None, [coinbase_trans], "Chain 2, Block 1 #")
    block_c3_valid_1 = mkBlock(None, [coinbase_trans], "Chain 3, Block 1 #")
    mine(block_c1_valid_1)
    mine(block_c2_valid_1)
    mine(block_c3_valid_1)
    coinbase_trans_2 = mkCoinbase(0,2,50000000000000)
    block_c1_valid_2 = mkBlock(block_c1_valid_1, [coinbase_trans_2], "Chain 1, Block 2")
    block_c2_valid_2 = mkBlock(block_c2_valid_1, [coinbase_trans_2], "Chain 2, Block 2")
    block_c3_valid_2 = mkBlock(block_c3_valid_1, [coinbase_trans_2], "Chain 3, Block 2")
    mine(block_c1_valid_2)
    mine(block_c2_valid_2)
    mine(block_c3_valid_2)
    coinbase_trans_3 = mkCoinbase(0,3,50000000000000)
    block_c1_valid_3 = mkBlock(block_c1_valid_2, [coinbase_trans_3], "Chain 1, Block 3")
    block_c2_valid_3 = mkBlock(block_c2_valid_2, [coinbase_trans_3], "Chain 2, Block 3")
    block_c3_valid_3 = mkBlock(block_c3_valid_2, [coinbase_trans_3], "Chain 3, Block 3")
    mine(block_c1_valid_3)
    mine(block_c2_valid_3)
    mine(block_c3_valid_3)
    coinbase_trans_4 = mkCoinbase(0,4,50000000000000)
    block_c1_valid_4 = mkBlock(block_c1_valid_3, [coinbase_trans_4], "Chain 1, Block 4")
    block_c2_valid_4 = mkBlock(block_c2_valid_3, [coinbase_trans_4], "Chain 2, Block 4")
    block_c3_valid_4 = mkBlock(block_c3_valid_3, [coinbase_trans_4], "Chain 3, Block 4")
    mine(block_c1_valid_4)
    mine(block_c2_valid_4)
    mine(block_c3_valid_4)
    coinbase_trans_5 = mkCoinbase(0,5,50000000000000)
    block_c1_valid_5 = mkBlock(block_c1_valid_4, [coinbase_trans_5], "Chain 1, Block 5")
    block_c2_valid_5 = mkBlock(block_c2_valid_4, [coinbase_trans_5], "Chain 2, Block 5")
    block_c3_valid_5 = mkBlock(block_c3_valid_4, [coinbase_trans_5], "Chain 3, Block 5")
    mine(block_c1_valid_5)
    mine(block_c2_valid_5)
    mine(block_c3_valid_5)
    return {
            'description': description,
            'ignore_errors': [ 'UNFINDABLE_OBJECT' ],
            'objects': [ coinbase_trans, coinbase_trans_2, coinbase_trans_3, coinbase_trans_4, coinbase_trans_5, (block_c1_valid_1,True), block_c3_valid_1, block_c1_valid_2, (block_c2_valid_2,False), block_c3_valid_2, getchaintip(block_c1_valid_1), block_c1_valid_3, block_c2_valid_3, (block_c3_valid_3,True), getchaintip(block_c3_valid_3), (block_c1_valid_4,True), getchaintip(block_c1_valid_4), block_c2_valid_4, block_c3_valid_4, block_c1_valid_5, (block_c2_valid_5,False), block_c3_valid_5, getchaintip(block_c1_valid_4) ]
    }
