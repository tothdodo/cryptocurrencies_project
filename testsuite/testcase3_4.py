from v import *

coinbase_trans = {"object":{"height":1,"outputs":[{"pubkey":pubkeys[0],"value":50000000000000}],"type":"transaction"},"type":"object"}

def gen_test_more_output_input():
    description = "A transaction creates more output than it has input"
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    coinbase_trans_1 = mkCoinbase(1, 2, 50000000000000)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans,0)],[transOut(3, 50000000000001)])
    full_signature(0, transfer_trans_2)
    mine(block_valid_1)
    block_invalid_2 = mkBlock(block_valid_1, [coinbase_trans_1, transfer_trans_2], description)
    return {
            'description' : description,
            'expected': 'INVALID_TX_CONSERVATION',
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, (block_valid_1,True), (block_invalid_2,False) ]
            }

# we transfer coinbase transactions to multiple wallets and then
# move merge all these wallets together to wallet 5
def gen_test_valid_multikey():
    description = "Multiple transactions with multiple keys"
    Bv1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    mine(Bv1)
    T_cb_2 = mkCoinbase(1, 2, 50000000000000)
    T_tt_2 = mkTrans([transIn(0,coinbase_trans,0)],[transOut(2,25000000000000),transOut(3,25000000000000)])
    full_signature (0, T_tt_2)
    Bv2 = mkBlock(Bv1, [T_cb_2,T_tt_2], description)
    mine(Bv2)
    T_cb_3 = mkCoinbase(4, 3, 50000000000000)
    T_tt_3 = mkTrans([transIn(0,T_cb_2),transIn(0,T_tt_2),transIn(1,T_tt_2)],[transOut(5,100000000000000)])
    diff_signature([1,2,3], T_tt_3)
    Bv3 = mkBlock(Bv2, [T_cb_3, T_tt_3], description)
    return {
            'description': description,
            'objects': [ coinbase_trans, (Bv1,True), T_cb_2, T_tt_2, (Bv2,True), T_cb_3, T_tt_3, (Bv3,True) ]
            }
    
#def gen_test_double_spend1():
#    description = "A transaction spends coinbase from same block"
#    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
#    mine(block_valid_1)
#    coinbase_trans_1 = mkCoinbase(0, 2, 50000000000000)
#    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans,0),transIn(0,coinbase_trans_1,0)],[transOut(3, 100000000000000)])
#    full_signature(0, transfer_trans_2)
#    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_1, transfer_trans_2], description)
#    mine(block_valid_2)
#    coinbase_trans_2 = mkCoinbase(1, 3, 50000000000000)
#    transfer_trans_3 = mkTrans([transIn(0,coinbase_trans,0)],[transOut(3, 100000000000000)])
#    block_invalid_3 = mkBlock(block_valid_2, [coinbase_trans_2, transfer_trans_3], description)
#    return {
#            'description' : description,
#            'expected': 'INVALID_TX_CONSERVATION',
#            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, (block_valid_1,True), (block_invalid_2,False) ]
#            }

def gen_test_double_spend2():
    description = "A transaction spends coinbase from same block"
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    coinbase_trans_1 = mkCoinbase(0, 2, 50000000000000)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans), transIn(0,coinbase_trans_1)],[transOut(3, 100000000000000)])
    full_signature(0, transfer_trans_2)
    mine(block_valid_1)
    block_invalid_2 = mkBlock(block_valid_1, [coinbase_trans_1, transfer_trans_2], description)
    return {
            'description' : description,
            'expected': 'INVALID_TX_OUTPOINT',
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, (block_valid_1,True), (block_invalid_2,False) ]
            }

def gen_test_two_chains():
    description = "Sending two valid chains"
    block_valid_11 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction#1")
    block_valid_12 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction#2")
    mine(block_valid_11)
    mine(block_valid_12)
    coinbase_trans_11 = mkCoinbase(0, 2, 50000000000000)
    transfer_trans_21 = mkTrans([transIn(0,coinbase_trans)],[transOut(3, 25000000000000),transOut(4, 25000000000000)])
    transfer_trans_22 = mkTrans([transIn(0,coinbase_trans)],[transOut(3, 25000000000000),transOut(4, 25000000000000)])
    full_signature(0, transfer_trans_21)
    full_signature(0, transfer_trans_22)
    block_valid_21 = mkBlock(block_valid_11, [coinbase_trans_11,transfer_trans_21], description)
    block_valid_22 = mkBlock(block_valid_12, [coinbase_trans_11,transfer_trans_22], description)
    mine(block_valid_21)
    mine(block_valid_22)
    transfer_trans_31 = mkTrans([transIn(1,transfer_trans_21)],[transOut(5,12500000000000),transOut(6,12500000000000)])
    transfer_trans_32 = mkTrans([transIn(1,transfer_trans_22)],[transOut(5,12500000000000),transOut(6,12500000000000)])
    full_signature(4, transfer_trans_31)
    full_signature(4, transfer_trans_32)
    block_valid_31 = mkBlock(block_valid_21, [transfer_trans_31], description)
    block_valid_32 = mkBlock(block_valid_22, [transfer_trans_32], description)
    return {
            'description' : description,
            'objects': [ coinbase_trans, coinbase_trans_11, transfer_trans_21, transfer_trans_22, transfer_trans_31, transfer_trans_32, (block_valid_11,True), (block_valid_12,True), (block_valid_21,True), (block_valid_22,True), (block_valid_31,True), (block_valid_32,True) ]
            }

def gen_test_wrong_chain_input():
    description = "Sending two valid chains"
    block_valid_11 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction#1")
    block_valid_12 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction#2")
    mine(block_valid_11)
    mine(block_valid_12)
    coinbase_trans_11 = mkCoinbase(0, 2, 50000000000000)
    transfer_trans_21 = mkTrans([transIn(0,coinbase_trans)],[transOut(2, 25000000000000),transOut(4, 25000000000000)])
    transfer_trans_22 = mkTrans([transIn(0,coinbase_trans)],[transOut(3, 25000000000000),transOut(4, 25000000000000)])
    full_signature(0, transfer_trans_21)
    full_signature(0, transfer_trans_22)
    block_valid_21 = mkBlock(block_valid_11, [coinbase_trans_11,transfer_trans_21], description)
    block_valid_22 = mkBlock(block_valid_12, [coinbase_trans_11,transfer_trans_22], description)
    mine(block_valid_21)
    mine(block_valid_22)
    transfer_trans_31 = mkTrans([transIn(1,transfer_trans_21)],[transOut(5,12500000000000),transOut(6,12500000000000)])
    transfer_trans_32 = mkTrans([transIn(1,transfer_trans_22)],[transOut(5,12500000000000),transOut(6,12500000000000)])
    full_signature(4, transfer_trans_31)
    full_signature(4, transfer_trans_32)
    block_invalid_31 = mkBlock(block_valid_21, [transfer_trans_32], description)
    return {
            'description' : description,
            'expected': 'INVALID_TX_OUTPOINT',
            'objects': [ coinbase_trans, coinbase_trans_11, transfer_trans_21, transfer_trans_22, transfer_trans_31, transfer_trans_32, (block_valid_11,True), (block_valid_12,True), (block_valid_21,True), (block_valid_22,True), (block_invalid_31,False) ]
            }


def gen_test_right_txid_output():
    description = "A transaction references invalid txid outpoint"
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    mine(block_valid_1)
    coinbase_trans_1 = mkCoinbase(0, 2, 50000000000000)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans)],[transOut(1, 10000000000000),transOut(2, 10000000000000),transOut(3, 10000000000000),transOut(4, 10000000000000)])
    full_signature(0, transfer_trans_2)
    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_1, transfer_trans_2], description)
    mine(block_valid_2)
    transfer_trans_3 = mkTrans([transIn(3,transfer_trans_2)],[transOut(7, 100)])
    full_signature(4, transfer_trans_3)
    block_valid_3 = mkBlock(block_valid_2, [transfer_trans_3], description)
    return {
            'description' : description,
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, transfer_trans_3, (block_valid_1,True), (block_valid_2,True), (block_valid_3,True) ]
            }


def gen_test_wrong_txid_output():
    description = "A transaction references invalid txid outpoint"
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    mine(block_valid_1)
    coinbase_trans_1 = mkCoinbase(0, 2, 50000000000000)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans)],[transOut(1, 10000000000000),transOut(2, 10000000000000),transOut(3, 10000000000000),transOut(4, 10000000000000)])
    full_signature(0, transfer_trans_2)
    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_1, transfer_trans_2], description)
    mine(block_valid_2)
    transfer_trans_3 = mkTrans([transIn(4,transfer_trans_2)],[transOut(7, 100)])
    full_signature(4, transfer_trans_3)
    block_invalid_3 = mkBlock(block_valid_2, [transfer_trans_3], description)
    return {
            'description' : description,
            'expected': 'INVALID_TX_OUTPOINT',
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, transfer_trans_3, (block_valid_1,True), (block_valid_2,True), (block_invalid_3,False) ]
            }


def gen_test_invalid_sig():
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    coinbase_trans_1 = mkCoinbase(1, 2, 50000000000100)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans,1)],[transOut(3, 49999999999900)])
    full_signature(1, transfer_trans_2)
    block_invalid_2 = mkBlock(block_valid_1, [coinbase_trans_1,transfer_trans_2], 'This block has tx with invalid sigs')
    return {
            'description' : 'Invalid signature',
            'expected': 'INVALID_TX_SIGNATURE',
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, (block_valid_1,True), (block_invalid_2,False) ]
            }

def gen_test_invalid_timestamp1():
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    coinbase_trans_1 = mkCoinbase(1, 2, 50000000000100)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans,1)],[transOut(3, 49999999999900)])
    full_signature(0, transfer_trans_2)
    block_invalid_2 = mkBlock(block_valid_1, [coinbase_trans_1,transfer_trans_2], 'This block has invalid timestamp')
    block_invalid_2['object']['created'] = block_valid_1['object']['created']
    return {
            'description' : 'Invalid Timestamp',
            'expected': 'INVALID_BLOCK_TIMESTAMP',
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, (block_valid_1,True), (block_invalid_2,False) ]
            }

def gen_test_invalid_timestamp2():
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    coinbase_trans_1 = mkCoinbase(1, 2, 50000000000100)
    transfer_trans_2 = mkTrans([transIn(0,coinbase_trans,1)],[transOut(3, 49999999999900)])
    full_signature(0, transfer_trans_2)
    block_invalid_2 = mkBlock(block_valid_1, [coinbase_trans_1,transfer_trans_2], 'This block has invalid timestamp (future)')
    block_invalid_2['object']['created'] = 1795730645
    return {
            'description' : 'Invalid Timestamp (future)',
            'expected': 'INVALID_BLOCK_TIMESTAMP',
            'objects': [ coinbase_trans, coinbase_trans_1, transfer_trans_2, (block_valid_1,True), (block_invalid_2,False) ]
            }

