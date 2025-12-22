from v import *

coinbase_trans = {"object":{"height":1,"outputs":[{"pubkey":pubkeys[0],"value":50000000000000}],"type":"transaction"},"type":"object"}
block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
transfer_trans_2 = mkTrans([transIn(0,coinbase_trans)],[transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000)])
full_signature (0, transfer_trans_2)

def gen_test_1_mempool_basic():
    description = "Send transaction, expect it in mempool"
    coinbase_trans_1 = mkCoinbase(0,3,50000000000000)
    return {
            'description' : description,
            'objects': [ coinbase_trans, (block_valid_1,True), coinbase_trans_1, transfer_trans_2, mempool([transfer_trans_2]), getmempool([transfer_trans_2])
            ]
    }

def gen_test_2_mempool_advanced():
    description = "Send 2 transactions, expect them in mempool"
    coinbase_trans_1 = mkCoinbase(0,2,50000000000000)
    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_1, transfer_trans_2], "Transfer block")
    mine(block_valid_2)

    transfer_trans_3_1 = mkTrans([transIn(0,transfer_trans_2)],[transOut(1,12500000000000)])
    transfer_trans_3_2 = mkTrans([transIn(1,transfer_trans_2)],[transOut(1,12500000000000)])
    full_signature (0, transfer_trans_3_1)
    full_signature (0, transfer_trans_3_2)

    return {
            'description' : description,
            'objects': [ coinbase_trans, (block_valid_1,False), (transfer_trans_2,True), getmempool([transfer_trans_2]),  (block_valid_2,True), coinbase_trans_1, (transfer_trans_3_1,False), (transfer_trans_3_2,False), getmempool([transfer_trans_3_1,transfer_trans_3_2])
            ]
    }

# sending a blockid instead of a txid in mempool has no clearly defined expected behaviour
# but we can at least assume that it should not show up in the resulting mempool
def gen_test_3_mempool_send_block():
    description = "Send block in mempool"
    coinbase_trans_2 = mkCoinbase(1,2,50000000000000)
    transfer_trans_3 = mkTrans([transIn(2,transfer_trans_2)],[transOut(2,12500000000000)])
    full_signature(0, transfer_trans_3)
    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_2, transfer_trans_2], "Valid block")
    mine(block_valid_2)
    return {
            'description': description,
            'objects': [ coinbase_trans, block_valid_1, transfer_trans_2, transfer_trans_3, block_valid_2, coinbase_trans_2, mempool([block_valid_2, transfer_trans_3]), mempool_include_exclude([transfer_trans_3],[block_valid_2])
                        ]
            }

def gen_test_4_mempool_coinbase():
    coinbase_trans_2 = mkCoinbase(1,3,50000000000000)
    return {
            'description': 'Send coinbase, shall not be in mempool',
            'objects': [ (coinbase_trans_2,True), mempool_excludes([coinbase_trans_2]) ]
            }

def gen_test_5_mempool_competing():
    coinbase_trans_2 = mkCoinbase(2,2,50000000000000)
    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_2,transfer_trans_2], "Valid Block #2")
    mine(block_valid_2)
    transfer_trans_3_1 = mkTrans([transIn(0, transfer_trans_2)],[transOut(1,12500000000000)])
    transfer_trans_3_2 = mkTrans([transIn(0, transfer_trans_2)],[transOut(2,12500000000000)])
    full_signature(0, transfer_trans_3_1)
    full_signature(0, transfer_trans_3_2)

    return {
            'description': 'Two transaction compete to get in mempool, only first should make it',
            'objects': [  coinbase_trans, block_valid_1, transfer_trans_2, (block_valid_2,True), coinbase_trans_2, (transfer_trans_3_1,True), (transfer_trans_3_2,True), mempool_include_exclude([transfer_trans_3_1], [transfer_trans_3_2]) ]
            }

# create new chain, old mempool, shall get flushed after block 3 is new longest chain
def gen_test_6_mempool_empty_after_block():
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a new valid coinbase transaction")
    coinbase_trans_2 = mkCoinbase(2,2,50000000000000)
    transfer_trans_X = mkTrans([transIn(0,coinbase_trans)],[transOut(0,12500000000000),transOut(0,12500000000000)])
    full_signature(0, transfer_trans_X)
    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_2,transfer_trans_X], "Valid Block #2")
    transfer_trans_3_1 = mkTrans([transIn(0, transfer_trans_X)],[transOut(1,12400000000000)])
    transfer_trans_3_2 = mkTrans([transIn(1, transfer_trans_X)],[transOut(2,12300000000000)])
    transfer_trans_3_3 = mkTrans([transIn(3, transfer_trans_2)],[transOut(3,12200000000000)])
    full_signature(0, transfer_trans_3_1)
    full_signature(0, transfer_trans_3_2)
    full_signature(0, transfer_trans_3_3)
    block_valid_3 = mkBlock(block_valid_2, [transfer_trans_3_1,transfer_trans_3_2], "Valid Block #3")
    mine(block_valid_3)
    return {
            'description': 'Flush transactions with block, mempool empty',
            'objects': [  coinbase_trans, block_valid_1, transfer_trans_X, block_valid_2, coinbase_trans_2, (transfer_trans_3_1,True), (transfer_trans_3_2,True), (transfer_trans_3_3,False), mempool_include_exclude([transfer_trans_3_3],[transfer_trans_3_1,transfer_trans_3_2]), (block_valid_3,True), getmempool([]) ]
            }

coinbase_trans_2 = None
block_valid_3 = None
block_valid_4 = None
tx_cb2_c2_xor_c3 = None
tx_cb2_c3_xor_c2 = None
tx_a1_1 = None
tx_a1_2 = None
tx_a1_3 = None
tx_cb1_4_c1_1 = None

# extend chain 1 to be longest chain w/ 4 blocks
def gen_test_rebase_1():
    global block_valid_3, block_valid_4, tx_a1_1, tx_cb1_4_c1_1, tx_a1_2, tx_a1_3, coinbase_trans_2
    coinbase_trans_1 = mkCoinbase(1,1,50000000000000)
    block_valid_1 = mkBlock(None, [coinbase_trans_1], "Rebase: Valid Block #1")
    tx_split_cb1_4 = mkTrans([transIn(0, coinbase_trans_1)],[transOut(1,5000000000000),transOut(1,12500000000000),transOut(1,17500000000000),transOut(1,15000000000000)])
    full_signature(1, tx_split_cb1_4)
    coinbase_trans_2 = mkCoinbase(1,2,50000000000000)
    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_2,tx_split_cb1_4], "Rebase: Valid Block #2")

    tx_a1_1 = mkTrans([transIn(0,tx_split_cb1_4)],[transOut(1,800000000000),transOut(1,1200000000000),transOut(1,1400000000000),transOut(1,1600000000000)])
    full_signature(1, tx_a1_1)
    tx_a1_2 = mkTrans([transIn(2,tx_split_cb1_4)],[transOut(1,17500000000000)])
    full_signature(1, tx_a1_2)
    tx_a1_3 = mkTrans([transIn(3,tx_split_cb1_4)],[transOut(1,15000000000000)])
    full_signature(1, tx_a1_3)
    coinbase_trans_3 = mkCoinbase(1,3,50000000000000)
    block_valid_3 = mkBlock(block_valid_2, [coinbase_trans_3], "Rebase: Valid Block #3")

    coinbase_trans_4 = mkCoinbase(1,4,50000000000000)
    block_valid_4 = mkBlock(block_valid_3, [coinbase_trans_4], "Rebase: Valid Block #4")
    mine(block_valid_4)
    tx_cb1_4_c1_1 = mkTrans([transIn(1,tx_split_cb1_4)],[transOut(1,12500000000000)])
    full_signature(1, tx_cb1_4_c1_1)

    return {
            'description': "Rebase 1: new longest chain, mempool 2 tx",
            'objects': [ coinbase_trans_1, coinbase_trans_2, coinbase_trans_3, coinbase_trans_4, block_valid_1, block_valid_2, block_valid_3, tx_split_cb1_4, (block_valid_4,False), getchaintip(block_valid_4), (tx_cb1_4_c1_1,False), (tx_a1_1,False), getmempool([tx_cb1_4_c1_1,tx_a1_1]), tx_a1_2, tx_a1_3 ]
    }

# extend chain 2 to be longest chain w/ 5 blocks, LCA=#4
def gen_test_rebase_2():
    global block_valid_3, tx_cb2_c2_xor_c3, tx_cb1_4_c1_1, coinbase_trans_2
    coinbase_trans_4 = mkCoinbase(1,4,50000000000000)
    block_valid_c2_4 = mkBlock(block_valid_3, [coinbase_trans_4], "Rebase: Chain 2, Block #4")
    coinbase_trans_c2_5 = mkCoinbase(1,5,50000000000000)
    tx_cb2_c2_xor_c3 = mkTrans([transIn(0, coinbase_trans_2)],[transOut(1,20000000000000),transOut(1,30000000000000)])
    full_signature(1, tx_cb2_c2_xor_c3)
    block_valid_c2_5 = mkBlock(block_valid_c2_4, [coinbase_trans_c2_5], "Rebase: Chain 2, Block #5")
    mine(block_valid_c2_5)

    return {
            'description': "Rebase 2: longest chain = C2, mempool = [2 tx from C1, 1 tx from C2]",
            'objects': [ coinbase_trans_4, block_valid_c2_4, coinbase_trans_c2_5, (block_valid_c2_5,False), (tx_cb2_c2_xor_c3,False), getchaintip(block_valid_c2_5), getmempool([tx_cb1_4_c1_1,tx_a1_1,tx_cb2_c2_xor_c3])
                        ]
            }

# extend chain 3 from LCA=#4
def gen_test_rebase_3():
    global block_valid_c3_6, block_valid_4, coinbase_trans_2, tx_a1_2, tx_cb2_c3_xor_c2
    coinbase_trans_c3_5 = mkCoinbase(1,5,50000000000000)
    tx_cb2_c3_xor_c2 = mkTrans([transIn(0, coinbase_trans_2)],[transOut(1,30000000000000),transOut(1,20000000000000)])
    full_signature(1, tx_cb2_c3_xor_c2)
    block_valid_c3_5 = mkBlock(block_valid_4, [coinbase_trans_c3_5,tx_cb2_c3_xor_c2], "Rebase: Chain 3, Block #5")
    tx_cb35_1 = mkTrans([transIn(0,coinbase_trans_c3_5)],[transOut(1,50000000000000)])
    full_signature(1, tx_cb35_1)
    coinbase_trans_c3_6 = mkCoinbase(1,6,50000000000000)
    block_valid_c3_6 = mkBlock(block_valid_c3_5, [coinbase_trans_c3_6], "Rebase: Chain 3, Block #6")
    mine(block_valid_c3_6)
    
    return {
            'description': "Rebase 3: longest chain = C3, mempool = [1 tx from C1, 1 tx from C3, 2 gen tx]",
            'objects': [ coinbase_trans_c3_5, tx_cb2_c3_xor_c2, block_valid_c3_5, coinbase_trans_c3_6, (block_valid_c3_6,False), (tx_cb35_1,False), (tx_a1_2,False), getchaintip(block_valid_c3_6), getmempool([tx_cb1_4_c1_1,tx_a1_1,tx_cb35_1,tx_a1_2]) ]
            }

# extend chain 1 from LCA=#4
def gen_test_rebase_4():
    global block_valid_4,tx_cb2_c3_xor_c2,tx_cb1_4_c1_1,tx_a1_1,tx_cb35_1,tx_a1_2,tx_a1_3
    coinbase_trans_c1_5 = mkCoinbase(5,5,50000000000000)
    block_valid_c1_5 = mkBlock(block_valid_4, [coinbase_trans_c1_5], "Rebase: Chain 1, Block #5")
    coinbase_trans_c1_6 = mkCoinbase(2,6,50000000000000)
    block_valid_c1_6 = mkBlock(block_valid_c1_5, [coinbase_trans_c1_6], "Rebase: Chain 1, Block #6")
    coinbase_trans_c1_7 = mkCoinbase(2,7,50000000000000)
    block_valid_c1_7 = mkBlock(block_valid_c1_6, [coinbase_trans_c1_7], "Rebase: Chain 1, Block #7")
    mine(block_valid_c1_7)

    return {
            'description': "Rebase 4: longest chain = C1, mempool = [1 tx from C1, 1 tx from C3, 3 gen tx]",
            'objects': [ (tx_a1_3,False), coinbase_trans_c1_5, block_valid_c1_5, coinbase_trans_c1_6, block_valid_c1_6, coinbase_trans_c1_7, block_valid_c1_7, chaintip(block_valid_c1_7), getchaintip(block_valid_c1_7), getmempool([tx_cb2_c3_xor_c2,tx_cb1_4_c1_1,tx_a1_1,tx_a1_2,tx_a1_3]) ]
    }

# extend chain 3 from LCA=#4, use all open tx
def gen_test_rebase_5():
    global block_valid_c3_6,tx_cb1_4_c1_1,tx_a1_1,tx_a1_2,tx_a1_3
    block_valid_c3_7 = mkBlock(block_valid_c3_6, [tx_cb1_4_c1_1,tx_a1_1,tx_a1_2,tx_a1_3], "Rebase: Chain 3, Block #7")
    coinbase_trans_c3_8 = mkCoinbase(2,8,50000000000000)
    block_valid_c3_8 = mkBlock(block_valid_c3_7, [coinbase_trans_c3_8], "Rebase: Chain 3, Block #8")
    mine(block_valid_c3_8)

    return {
            'description': "Rebase 5: longest chain = C3, mempool = []",
            'objects': [ block_valid_c3_6,tx_cb1_4_c1_1,tx_a1_1,tx_a1_2,tx_a1_3,block_valid_c3_7,coinbase_trans_c3_8, (block_valid_c3_8,False), getchaintip(block_valid_c3_8), getmempool([]) ]
            }

#coinbase_trans_2 = mkCoinbase(3,2,50000000000000)
#coinbase_trans_3 = mkCoinbase(4,3,50000000000000)
#coinbase_trans_4 = mkCoinbase(5,4,50000000000000)
#coinbase_trans_5 = mkCoinbase(0,5,50000000000000)
#coinbase_trans_6 = mkCoinbase(0,6,50000000000000)
#coinbase_trans_7 = mkCoinbase(0,7,50000000000000)
#coinbase_trans_8 = mkCoinbase(0,8,50000000000000)
#block_valid_2 = None
#block_valid_3 = None
#block_valid_4 = None
#block_chain1_valid_5 = None
#block_chain1_valid_5 = None
#tx_coinbase_2 = mkTrans([transIn(0, coinbase_trans_2)],[transOut(3, 25000000000000),transOut(3, 25000000000000)])
#full_signature(3, tx_coinbase_2)
#transfer_trans_5_1 = mkTrans([transIn(0, tx_coinbase_2)], [transOut(0, 12500000000000),transOut(0, 12500000000000)])
#full_signature(3, transfer_trans_5_1)
#transfer_trans_5_2 = mkTrans([transIn(0, tx_coinbase_2)], [transOut(0, 20000000000000),transOut(0, 5000000000000)])
#full_signature(3, transfer_trans_5_2)
#
#transfer_trans_6_a1 = mkTrans([transIn(0, coinbase_trans_3)], [transOut(0, 25000000000000),transOut(0, 25000000000000)])
#full_signature(4, transfer_trans_6_a1)
#transfer_trans_6_2 = mkTrans([transIn(0, transfer_trans_5_1),transIn(1, transfer_trans_5_1)], [transOut(0, 2500000000000),transOut(0, 2500000000000)])
#full_signature(0, transfer_trans_6_2)
#transfer_trans_7_a1 = mkTrans([transIn(0, transfer_trans_6_a1)], [transOut(0, 12500000000000),transOut(0, 12500000000000)])
#full_signature(0, transfer_trans_7_a1)
#
#
#def gen_test_6_mempool_rebase_chain_1():
#    global coinbase_trans_2, coinbase_trans_3,tx_coinbase_2, coinbase_trans_4, block_valid_2, block_valid_1, block_valid_3, block_valid_4, block_chain1_valid_5
#    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_2], "Valid Block #2,6")
#    block_valid_3 = mkBlock(block_valid_2, [coinbase_trans_3,tx_coinbase_2], "Valid Block #3,6")
#    block_valid_4 = mkBlock(block_valid_3, [coinbase_trans_4], "Valid Block #4,6")
#    mine(block_valid_4)
#    # transfer_trans_5_1 and transfer_trans_5_2 are mutually exclusive
#    block_chain1_valid_5 = mkBlock(block_valid_4, [transfer_trans_5_1, transfer_trans_6_a1], "Valid Block #5, Chain 1")
#    mine(block_chain1_valid_5)
#    # chain1 is longest chain
#    return {
#            'description': 'Three chains, changing chaintips, changing mempools #1',
#            'objects': [
#    coinbase_trans, coinbase_trans_2, tx_coinbase_2, coinbase_trans_3, coinbase_trans_4, coinbase_trans_5, coinbase_trans_6, coinbase_trans_7, coinbase_trans_8, block_valid_1, block_valid_2, block_valid_3, (block_valid_4,False), (transfer_trans_5_1,False), (transfer_trans_5_2,False), mempool_include_exclude([transfer_trans_5_1],[transfer_trans_5_2]), (block_chain1_valid_5,False), (transfer_trans_6_2,False), getchaintip(block_chain1_valid_5), transfer_trans_6_a1, mempool_include_exclude([transfer_trans_6_2],[transfer_trans_5_1,transfer_trans_6_a1])#,
##    block_chain2_valid_4, block_chain2_valid_5, (transfer_trans_c2_6,False), (transfer_trans_7_a1,False), mempool_include_exclude([transfer_trans_7_a1],[transfer_trans_c2_6]), (block_chain2_valid_6,True), getchaintip(block_chain2_valid_6), mempool_excludes([transfer_trans_7_a1,transfer_trans_c2_6]),
##    block_chain1_valid_6, (block_chain1_valid_7,False), getchaintip(block_chain1_valid_7), mempool_include_exclude([transfer_trans_7_a1],[transfer_trans_5_2]),
##    block_chain3_valid_5, block_chain3_valid_6, chaintip(block_chain3_valid_6), block_chain3_valid_7, block_chain3_valid_8, chaintip(block_chain3_valid_8), mempool_include_exclude([transfer_trans_7_a1,transfer_trans_5_1, transfer_trans_6_a1], [coinbase_trans, coinbase_trans_2, coinbase_trans_3, coinbase_trans_4, coinbase_trans_5, coinbase_trans_6, coinbase_trans_7, coinbase_trans_8,transfer_trans_5_2])
#            ]
#            }
#
#
#def gen_test_6_mempool_rebase_chain_2():
#    global block_chain2_valid_4, block_valid_3, coinbase_trans_4, transfer_trans_5_2, block_chain2_valid_5, block_chain2_valid_6, block_chain2_valid_4, coinbase_trans_6, transfer_trans_7_a1, tx_coinbase_2, transfer_trans_6_a1, coinbase_trans_3
#    block_chain2_valid_4 = mkBlock(block_valid_3, [coinbase_trans_4, transfer_trans_5_2], "Block Valid #4, Chain 2")
#    transfer_trans_c2_6 = mkTrans([transIn(0,transfer_trans_5_2)],[transOut(0, 2000000000000)])
#    full_signature(0, transfer_trans_c2_6)
#    block_chain2_valid_5 = mkBlock(block_chain2_valid_4, [transfer_trans_c2_6, transfer_trans_7_a1], "Block Valid #5, Chain 2")
#    block_chain2_valid_6 = mkBlock(block_chain2_valid_5, [coinbase_trans_6], "Block Valid #6, Chain 2")
#    mine(block_chain2_valid_6)
#    # now chain2 is longest chain (LCA = Block 3)
#    return {
#            'description': 'Three chains, changing chaintips, changing mempools #2',
#            'objects': [
#    transfer_trans_5_2, transfer_trans_6_a1,
#    coinbase_trans, coinbase_trans_2, tx_coinbase_2, coinbase_trans_3, coinbase_trans_4, coinbase_trans_5, coinbase_trans_6, coinbase_trans_7, coinbase_trans_8, block_valid_1, block_valid_2, block_valid_3, block_valid_4, #(transfer_trans_5_1,False), (transfer_trans_5_2,False), mempool_include_exclude([transfer_trans_5_1],[transfer_trans_5_2]), (block_chain1_valid_5,False), (transfer_trans_6_2,False), chaintip(block_chain1_valid_5), transfer_trans_6_a1, mempool_include_exclude([transfer_trans_6_2],[transfer_trans_5_1,transfer_trans_6_a1])#,
#    block_chain2_valid_4, block_chain2_valid_5, (transfer_trans_c2_6,False), (transfer_trans_7_a1,False), mempool_include_exclude([transfer_trans_7_a1],[transfer_trans_c2_6]), (block_chain2_valid_6,True), getchaintip(block_chain2_valid_6), mempool_excludes([transfer_trans_7_a1,transfer_trans_c2_6]),
##    block_chain1_valid_6, (block_chain1_valid_7,False), getchaintip(block_chain1_valid_7), mempool_include_exclude([transfer_trans_7_a1],[transfer_trans_5_2]),
##    block_chain3_valid_5, block_chain3_valid_6, chaintip(block_chain3_valid_6), block_chain3_valid_7, block_chain3_valid_8, chaintip(block_chain3_valid_8), mempool_include_exclude([transfer_trans_7_a1,transfer_trans_5_1, transfer_trans_6_a1], [coinbase_trans, coinbase_trans_2, coinbase_trans_3, coinbase_trans_4, coinbase_trans_5, coinbase_trans_6, coinbase_trans_7, coinbase_trans_8,transfer_trans_5_2])
#            ]
#            }
#
#
#def gen_test_6_mempool_rebase_chain():
#    coinbase_trans_2 = mkCoinbase(3,2,50000000000000)
#    coinbase_trans_3 = mkCoinbase(4,3,50000000000000)
#    coinbase_trans_4 = mkCoinbase(5,4,50000000000000)
#    coinbase_trans_5 = mkCoinbase(0,5,50000000000000)
#    coinbase_trans_6 = mkCoinbase(0,6,50000000000000)
#    coinbase_trans_7 = mkCoinbase(0,7,50000000000000)
#    coinbase_trans_8 = mkCoinbase(0,8,50000000000000)
#    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_2], "Valid Block #2,6")
#    tx_coinbase_2 = mkTrans([transIn(0, coinbase_trans_2)],[transOut(3, 25000000000000),transOut(3, 25000000000000)])
#    full_signature(3, tx_coinbase_2)
#    block_valid_3 = mkBlock(block_valid_2, [coinbase_trans_3,tx_coinbase_2], "Valid Block #3,6")
#    block_valid_4 = mkBlock(block_valid_3, [coinbase_trans_4], "Valid Block #4,6")
#    mine(block_valid_4)
#    # transfer_trans_5_1 and transfer_trans_5_2 are mutually exclusive
#    transfer_trans_5_1 = mkTrans([transIn(0, tx_coinbase_2)], [transOut(0, 12500000000000),transOut(0, 12500000000000)])
#    full_signature(3, transfer_trans_5_1)
#    transfer_trans_5_2 = mkTrans([transIn(1, tx_coinbase_2)], [transOut(0, 20000000000000),transOut(0, 5000000000000)])
#    full_signature(3, transfer_trans_5_2)
#
#    transfer_trans_6_a1 = mkTrans([transIn(0, coinbase_trans_3)], [transOut(0, 25000000000000),transOut(0, 25000000000000)])
#    full_signature(4, transfer_trans_6_a1)
#    transfer_trans_6_2 = mkTrans([transIn(0, transfer_trans_5_1),transIn(1, transfer_trans_5_1)], [transOut(0, 2500000000000),transOut(0, 2500000000000)])
#    full_signature(0, transfer_trans_6_2)
#    transfer_trans_7_a1 = mkTrans([transIn(0, transfer_trans_6_a1)], [transOut(0, 12500000000000),transOut(0, 12500000000000)])
#    full_signature(0, transfer_trans_7_a1)
#
#    block_chain1_valid_5 = mkBlock(block_valid_4, [transfer_trans_5_1, transfer_trans_6_a1], "Valid Block #5, Chain 1")
#    # chain1 is longest chain
#
#    block_chain2_valid_4 = mkBlock(block_valid_3, [coinbase_trans_4, transfer_trans_5_2], "Block Valid #4, Chain 2")
#    transfer_trans_c2_6 = mkTrans([transIn(0,transfer_trans_5_2)],[transOut(0, 2000000000000)])
#    full_signature(0, transfer_trans_c2_6)
#    block_chain2_valid_5 = mkBlock(block_chain2_valid_4, [transfer_trans_c2_6, transfer_trans_7_a1], "Block Valid #5, Chain 2")
#    block_chain2_valid_6 = mkBlock(block_chain2_valid_5, [coinbase_trans_6], "Block Valid #6, Chain 2")
#    mine(block_chain2_valid_6)
#    # now chain2 is longest chain (LCA = Block 3)
#
#    block_chain1_valid_6 = mkBlock(block_chain1_valid_5, [coinbase_trans_6], "Valid Block #6, Chain 1")
#    block_chain1_valid_7 = mkBlock(block_chain1_valid_6, [coinbase_trans_7], "Block Valid #7, Chain 1")
#    mine(block_chain1_valid_7)
#    # chain1 is again longest chain (LCA = Block 3)
#
#    block_chain3_valid_5 = mkBlock(block_valid_4, [coinbase_trans_5], "Block Valid #5, Chain 3")
#    block_chain3_valid_6 = mkBlock(block_chain3_valid_5, [coinbase_trans_6], "Block Valid #6, Chain 3")
#    block_chain3_valid_7 = mkBlock(block_chain3_valid_6, [coinbase_trans_7], "Block Valid #7, Chain 3")
#    block_chain3_valid_8 = mkBlock(block_chain3_valid_7, [coinbase_trans_8], "Block Valid #8, Chain 3")
#    mine(block_chain3_valid_8)
#    # now chain 3 is longest chain (LCA = Block 4)
#    return {
#            'description': 'Three chains, changing chaintips, changing mempools',
#            'objects': [
#    coinbase_trans, coinbase_trans_2, tx_coinbase_2, coinbase_trans_3, coinbase_trans_4, coinbase_trans_5, coinbase_trans_6, coinbase_trans_7, coinbase_trans_8, block_valid_1, block_valid_2, block_valid_3, (block_valid_4,False), (transfer_trans_5_1,False), (transfer_trans_5_2,False), mempool_include_exclude([transfer_trans_5_1],[transfer_trans_5_2]), (block_chain1_valid_5,False), (transfer_trans_6_2,False), chaintip(block_chain1_valid_5), transfer_trans_6_a1, mempool_include_exclude([transfer_trans_6_2],[transfer_trans_5_1,transfer_trans_6_a1]),
#    block_chain2_valid_4, block_chain2_valid_5, (transfer_trans_c2_6,False), (transfer_trans_7_a1,False), mempool_include_exclude([transfer_trans_7_a1],[transfer_trans_c2_6]), (block_chain2_valid_6,True), getchaintip(block_chain2_valid_6), mempool_excludes([transfer_trans_7_a1,transfer_trans_c2_6]),
#    block_chain1_valid_6, (block_chain1_valid_7,False), getchaintip(block_chain1_valid_7), mempool_include_exclude([transfer_trans_7_a1],[transfer_trans_5_2]),
#    block_chain3_valid_5, block_chain3_valid_6, chaintip(block_chain3_valid_6), block_chain3_valid_7, block_chain3_valid_8, chaintip(block_chain3_valid_8), mempool_include_exclude([transfer_trans_7_a1,transfer_trans_5_1, transfer_trans_6_a1], [coinbase_trans, coinbase_trans_2, coinbase_trans_3, coinbase_trans_4, coinbase_trans_5, coinbase_trans_6, coinbase_trans_7, coinbase_trans_8,transfer_trans_5_2])
#            ]
#            }
