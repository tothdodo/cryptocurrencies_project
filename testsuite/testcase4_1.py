from v import *

coinbase_trans = {"object":{"height":1,"outputs":[{"pubkey":pubkeys[0],"value":50000000000000}],"type":"transaction"},"type":"object"}

def gen_test_recursive_fetch_pass():
    description = "Recursive fetching of 5 blocks to genesis"
    coinbase_trans_2 = mkCoinbase(0, 2, 50000000000000)
    transfer_trans_3 = mkTrans([transIn(0,coinbase_trans),transIn(0,coinbase_trans_2)],[transOut(0,50000000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000)])
    full_signature (0, transfer_trans_3)
    transfer_trans_4_1 = mkTrans([transIn(0,transfer_trans_3)],[transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000)])
    full_signature (0, transfer_trans_4_1)
    transfer_trans_4_2 = mkTrans([transIn(1,transfer_trans_3),transIn(2,transfer_trans_3),transIn(3,transfer_trans_3),transIn(4,transfer_trans_3)],[transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000)])
    full_signature (0, transfer_trans_4_2)
    transfer_trans_5_1 = mkTrans([transIn(0,transfer_trans_4_1),transIn(1,transfer_trans_4_1),transIn(2,transfer_trans_4_1),transIn(3,transfer_trans_4_1)],[transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000)])
    full_signature (0, transfer_trans_5_1)
    transfer_trans_5_2 = mkTrans([transIn(0,transfer_trans_4_2),transIn(1,transfer_trans_4_2),transIn(2,transfer_trans_4_2),transIn(3,transfer_trans_4_2)],[transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000)])
    full_signature (1, transfer_trans_5_2)
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    mine(block_valid_1)
    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_2], "This block has a valid transaction")
    mine(block_valid_2)
    block_valid_3 = mkBlock(block_valid_2, [transfer_trans_3], "This block has a valid transaction")
    mine(block_valid_3)
    block_valid_4 = mkBlock(block_valid_3, [transfer_trans_4_1, transfer_trans_4_2], "This block has two valid transactions")
    mine(block_valid_4)
    block_valid_5 = mkBlock(block_valid_4, [transfer_trans_5_1, transfer_trans_5_2], "This block has two valid transactions")
    mine(block_valid_5)
    return {
            'description' : description,
            'objects': [ coinbase_trans, coinbase_trans_2, transfer_trans_3, transfer_trans_4_1, transfer_trans_4_2, transfer_trans_5_1, transfer_trans_5_2, block_valid_1, block_valid_2, block_valid_3, block_valid_4, block_valid_5, chaintip(block_valid_5), getchaintip(block_valid_5) 
            ]
    }


def gen_test_recursive_fetch_invalid_genesis():
    description = "Recursive fetching of 5 blocks to genesis"
    coinbase_trans_2 = mkCoinbase(0, 2, 50000000000000)
    transfer_trans_3 = mkTrans([transIn(0,coinbase_trans),transIn(0,coinbase_trans_2)],[transOut(0,50000000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000)])
    full_signature (0, transfer_trans_3)
    transfer_trans_4_1 = mkTrans([transIn(0,transfer_trans_3)],[transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000)])
    full_signature (0, transfer_trans_4_1)
    transfer_trans_4_2 = mkTrans([transIn(1,transfer_trans_3),transIn(2,transfer_trans_3),transIn(3,transfer_trans_3),transIn(4,transfer_trans_3)],[transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000)])
    full_signature (0, transfer_trans_4_2)
    transfer_trans_5_1 = mkTrans([transIn(0,transfer_trans_4_1),transIn(1,transfer_trans_4_1),transIn(2,transfer_trans_4_1),transIn(3,transfer_trans_4_1)],[transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000)])
    full_signature (0, transfer_trans_5_1)
    transfer_trans_5_2 = mkTrans([transIn(0,transfer_trans_4_2),transIn(1,transfer_trans_4_2),transIn(2,transfer_trans_4_2),transIn(3,transfer_trans_4_2)],[transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000)])
    full_signature (1, transfer_trans_5_2)
    block_invalid_0 = mkBlock(None, [], "This block is an invalid genesis block")
    block_invalid_0['object']['previd'] = None
    mine(block_invalid_0)
    block_valid_1 = mkBlock(block_invalid_0, [coinbase_trans], "This block has a valid coinbase transaction")
    mine(block_valid_1)
    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_2], "This block has a valid transaction")
    mine(block_valid_2)
    block_valid_3 = mkBlock(block_valid_2, [transfer_trans_3], "This block has a valid transaction")
    mine(block_valid_3)
    block_valid_4 = mkBlock(block_valid_3, [transfer_trans_4_1, transfer_trans_4_2], "This block has two valid transactions")
    mine(block_valid_4)
    block_valid_5 = mkBlock(block_valid_4, [transfer_trans_5_1, transfer_trans_5_2], "This block has two valid transactions")
    mine(block_valid_5)
    return {
            'description' : description,
            'expected': 'INVALID_ANCESTRY',
            'objects': [ coinbase_trans, coinbase_trans_2, transfer_trans_3, transfer_trans_4_1, transfer_trans_4_2, transfer_trans_5_1, transfer_trans_5_2, block_invalid_0, block_invalid_0, block_invalid_0, block_invalid_0, block_invalid_0, block_invalid_0, block_invalid_0, block_valid_1, block_valid_2, block_valid_3, block_valid_4, block_valid_5, chaintip(block_valid_5)
            ]
    }
def gen_test_recursive_fetch_invalid_tx():
    description = "Recursive fetching of 5 blocks, one tx is invalid"
    coinbase_trans_2 = mkCoinbase(0, 2, 50000000000000)
    transfer_trans_3 = mkTrans([transIn(0,coinbase_trans),transIn(0,coinbase_trans_2)],[transOut(0,50000000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000)])
    full_signature (1, transfer_trans_3)
    transfer_trans_4_1 = mkTrans([transIn(0,transfer_trans_3)],[transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000)])
    full_signature (0, transfer_trans_4_1)
    transfer_trans_4_2 = mkTrans([transIn(1,transfer_trans_3),transIn(2,transfer_trans_3),transIn(3,transfer_trans_3),transIn(4,transfer_trans_3)],[transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000)])
    full_signature (0, transfer_trans_4_2)
    transfer_trans_5_1 = mkTrans([transIn(0,transfer_trans_4_1),transIn(1,transfer_trans_4_1),transIn(2,transfer_trans_4_1),transIn(3,transfer_trans_4_1)],[transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000)])
    full_signature (0, transfer_trans_5_1)
    transfer_trans_5_2 = mkTrans([transIn(0,transfer_trans_4_2),transIn(1,transfer_trans_4_2),transIn(2,transfer_trans_4_2),transIn(3,transfer_trans_4_2)],[transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000)])
    full_signature (1, transfer_trans_5_2)
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    mine(block_valid_1)
    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_2], "This block has a valid transaction")
    mine(block_valid_2)
    block_valid_3 = mkBlock(block_valid_2, [transfer_trans_3], "This block has a valid transaction")
    mine(block_valid_3)
    block_valid_4 = mkBlock(block_valid_3, [transfer_trans_4_1, transfer_trans_4_2], "This block has two valid transactions")
    mine(block_valid_4)
    block_valid_5 = mkBlock(block_valid_4, [transfer_trans_5_1, transfer_trans_5_2], "This block has two valid transactions")
    mine(block_valid_5)
    return {
            'description' : description,
            'expected': 'INVALID_ANCESTRY',
            'objects': [ coinbase_trans, coinbase_trans_2, transfer_trans_3, transfer_trans_4_1, transfer_trans_4_2, transfer_trans_5_1, transfer_trans_5_2, block_valid_1, block_valid_2, block_valid_3, block_valid_4, block_valid_5, chaintip(block_valid_5)
            ]
    }


def gen_test_recursive_fetch_invalid_block():
    description = "Recursive fetching of 5 blocks, one block is invalid"
    coinbase_trans_2 = mkCoinbase(0, 2, 50000000000000)
    transfer_trans_3 = mkTrans([transIn(0,coinbase_trans),transIn(0,coinbase_trans_2)],[transOut(0,50000000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000)])
    full_signature (0, transfer_trans_3)
    transfer_trans_4_1 = mkTrans([transIn(0,transfer_trans_3)],[transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000)])
    full_signature (0, transfer_trans_4_1)
    transfer_trans_4_2 = mkTrans([transIn(1,transfer_trans_3),transIn(2,transfer_trans_3),transIn(3,transfer_trans_3),transIn(4,transfer_trans_3)],[transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000)])
    full_signature (0, transfer_trans_4_2)
    transfer_trans_5_1 = mkTrans([transIn(0,transfer_trans_4_1),transIn(1,transfer_trans_4_1),transIn(2,transfer_trans_4_1),transIn(3,transfer_trans_4_1)],[transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000)])
    full_signature (0, transfer_trans_5_1)
    transfer_trans_5_2 = mkTrans([transIn(0,transfer_trans_4_2),transIn(1,transfer_trans_4_2),transIn(2,transfer_trans_4_2),transIn(3,transfer_trans_4_2)],[transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000)])
    full_signature (1, transfer_trans_5_2)
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    mine(block_valid_1)
    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_2], "This block has a valid transaction")
    mine(block_valid_2)
    block_invalid_3 = mkBlock(block_valid_2, [transfer_trans_3], "This block has an invalid timestamp")
    block_invalid_3['object']['created'] = block_valid_2['object']['created']
    mine(block_invalid_3)
    block_valid_4 = mkBlock(block_invalid_3, [transfer_trans_4_1, transfer_trans_4_2], "This block has two valid transactions")
    mine(block_valid_4)
    block_valid_5 = mkBlock(block_valid_4, [transfer_trans_5_1, transfer_trans_5_2], "This block has two valid transactions")
    mine(block_valid_5)
    return {
            'description' : description,
            'expected': 'INVALID_ANCESTRY',
            'objects': [ coinbase_trans, coinbase_trans_2, transfer_trans_3, transfer_trans_4_1, transfer_trans_4_2, transfer_trans_5_1, transfer_trans_5_2, block_valid_1, block_valid_2, block_invalid_3, block_valid_4, block_valid_5, chaintip(block_valid_5) 
            ]
    }

def gen_test_recursive_fetch_timeout():
    description = "Recursive fetching of 5 blocks, one is missing"
    coinbase_trans_2 = mkCoinbase(0, 2, 50000000000000)
    transfer_trans_3 = mkTrans([transIn(0,coinbase_trans),transIn(0,coinbase_trans_2)],[transOut(0,50000000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000)])
    full_signature (0, transfer_trans_3)
    transfer_trans_4_1 = mkTrans([transIn(0,transfer_trans_3)],[transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000),transOut(0,12500000000000)])
    full_signature (0, transfer_trans_4_1)
    transfer_trans_4_2 = mkTrans([transIn(1,transfer_trans_3),transIn(2,transfer_trans_3),transIn(3,transfer_trans_3),transIn(4,transfer_trans_3)],[transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000)])
    full_signature (0, transfer_trans_4_2)
    transfer_trans_5_1 = mkTrans([transIn(0,transfer_trans_4_1),transIn(1,transfer_trans_4_1),transIn(2,transfer_trans_4_1),transIn(3,transfer_trans_4_1)],[transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000)])
    full_signature (0, transfer_trans_5_1)
    transfer_trans_5_2 = mkTrans([transIn(0,transfer_trans_4_2),transIn(1,transfer_trans_4_2),transIn(2,transfer_trans_4_2),transIn(3,transfer_trans_4_2)],[transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000),transOut(1,12500000000000)])
    full_signature (1, transfer_trans_5_2)
    block_valid_1 = mkBlock(None, [coinbase_trans], "This block has a valid coinbase transaction")
    mine(block_valid_1)
    block_valid_2 = mkBlock(block_valid_1, [coinbase_trans_2], "This block has a valid transaction")
    mine(block_valid_2)
    block_valid_3 = mkBlock(block_valid_2, [transfer_trans_3], "This block has a valid transaction")
    mine(block_valid_3)
    block_valid_4 = mkBlock(block_valid_3, [transfer_trans_4_1, transfer_trans_4_2], "This block has two valid transactions")
    mine(block_valid_4)
    block_valid_5 = mkBlock(block_valid_4, [transfer_trans_5_1, transfer_trans_5_2], "This block has two valid transactions")
    mine(block_valid_5)
    return {
            'description' : description,
            'expected': 'UNFINDABLE_OBJECT',
            'objects': [ coinbase_trans, coinbase_trans_2, transfer_trans_3, transfer_trans_4_1, transfer_trans_4_2, transfer_trans_5_1, transfer_trans_5_2, block_valid_2, block_valid_3, block_valid_4, (block_valid_5,False)
            ],
            'existing': [(block_valid_1,False),(block_valid_2,False),(block_valid_3,False),(block_valid_4,False),(block_valid_5,False)]
    }

