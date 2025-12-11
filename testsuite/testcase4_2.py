from v import *
import hashlib
import random

GENESIS_BLOCK = {
        "T":"0000abc000000000000000000000000000000000000000000000000000000000",
        "created":1671062400,
        "miner":"Marabu",
        "nonce":"00000000000000000000000000000000000000000000000000000000005bb0f2",
        "note":"The New York Times 2022-12-13: Scientists Achieve Nuclear Fusion Breakthrough With Blast of 192 Lasers",
        "previd": None,
        "txids":[],
        "type":"block"
}

coinbase_trans = {"object":{"height":1,"outputs":[{"pubkey":pubkeys[0],"value":50000000000000}],"type":"transaction"},"type":"object"}

def mine_transaction(tx):
    while (True):
        if (hashlib.blake2s(canonicalize(tx)).hexdigest().startswith('0000') and
            hashlib.blake2s(canonicalize(tx)).hexdigest()[4] <= '9'):
            return 
        tx['outputs'][0]['value'] += 1

def gen_test_valid_chaintip_genesis():
    description = "Send Genesis Block as chaintip"
    genesis = {'type':'object','object': GENESIS_BLOCK }
    return {
            'description': description,
            'objects': [ genesis, chaintip(genesis) ]
    }

def gen_test_invalid_chaintip_pow():
    description = "Send invalid pow block as chaintip"
    return {
            'description': description,
            'expected': 'INVALID_BLOCK_POW',
            'objects': [ chaintip("0001e402ab6db384b580b94c5ef8b352e2177b2b34b511d75c277646e3e877ec") ]
    }

def gen_test_invalid_format_chaintip():
    description = "Chaintip with transaction (invalid)"
    coinbase_trans_2 = mkCoinbase(0, 2, 0)
    mine_transaction(coinbase_trans_2['object'])
    return {
            'description' : description,
            'expected': 'INVALID_FORMAT',
            'objects': [ coinbase_trans, (coinbase_trans_2,True), chaintip(coinbase_trans_2)
            ]
    }

def gen_test_invalid_pow_parent_block():
    description = "Parent block with invalid POW"
    coinbase_trans_2 = mkCoinbase(1, 4, 0)
    block_invalid_1 = mkBlock(None, [coinbase_trans_2], description)
    block_invalid_1['object']['previd'] = "000d2a956862efbb621977bb9757e3ed5c95cb715fe0d79067fd301ea9dfb39c"
    mine(block_invalid_1)
    return {
            'description': description,
            'expected': 'INVALID_ANCESTRY',
            'objects': [ coinbase_trans_2, (block_invalid_1,False) ]
    }

def gen_test_tx_early_sig_check():
    description = "Block with early signature check"
    transfer_invalid_sig = mkTrans([transIn(0, coinbase_trans),transIn(1,"000d2a956862efbb621977bb9757e3ed5c95cb715fe0d79067fd301ea9dfb39c")],[transOut(1,50000)])
    full_signature (0, transfer_invalid_sig)
    transfer_invalid_sig['object']['inputs'][0]['sig'] = "000d2a956862efbb621977bb9757e3ed5c95cb715fe0d79067fd301ea9dfb39c000d2a956862efbb621977bb9757e3ed5c95cb715fe0d79067fd301ea9dfb39c"
    block_invalid_1 = mkBlock(None, [transfer_invalid_sig], description)
    mine(block_invalid_1)
    return {
            'description': description,
            'expected': 'INVALID_TX_SIGNATURE',
            'objects': [ coinbase_trans, transfer_invalid_sig, (block_invalid_1,False) ]
    }

def gen_test_tx_early_check2():
    description = "Block with early tx check (invalid index)"
    transfer_invalid_idx = mkTrans([transIn(1, coinbase_trans),transIn(1,"000d2a956862efbb621977bb9757e3ed5c95cb715fe0d79067fd301ea9dfb39c")],[transOut(1,50000)])
    full_signature (0, transfer_invalid_idx)
    block_invalid_1 = mkBlock(None, [transfer_invalid_idx], description)
    mine(block_invalid_1)
    return {
            'description': description,
            'expected': 'INVALID_TX_OUTPOINT',
            'objects': [ coinbase_trans, transfer_invalid_idx, (block_invalid_1,False) ]
    }

def gen_test_tx_early_check3():
    description = "Block with early tx check (invalid inputs)"
    block_valid_1 = mkBlock(None, [coinbase_trans], description)
    mine(block_valid_1)
    transfer_valid_inputs = mkTrans([transIn(0, coinbase_trans),transIn(1,"000d2a956862efbb621977bb9757e3ed5c95cb715fe0d79067fd301ea9dfb39c")],[transOut(1,50000)])
    transfer_invalid_inputs = mkTrans([],[])
    full_signature (0, transfer_valid_inputs)
    block_invalid_2 = mkBlock(block_valid_1, [transfer_valid_inputs,transfer_invalid_inputs], description)
    return {
            'description': description,
            'expected': 'INVALID_FORMAT',
            'objects': [ coinbase_trans, transfer_valid_inputs, transfer_invalid_inputs, block_valid_1, (block_invalid_2,False) ]
    }

def gen_test_tx_early_check4():
    description = "Block with early tx check (block in txids)"
    block_valid_1 = mkBlock(None, [coinbase_trans], description)
    mine(block_valid_1)
    transfer_valid_inputs = mkTrans([transIn(0, coinbase_trans),transIn(1,"000d2a956862efbb621977bb9757e3ed5c95cb715fe0d79067fd301ea9dfb39c")],[transOut(1,50000)])
    full_signature (0, transfer_valid_inputs)
    block_invalid_2 = mkBlock(block_valid_1, [transfer_valid_inputs,block_valid_1], description)
    return {
            'description': description,
            'expected': 'INVALID_FORMAT',
            'objects': [ transfer_valid_inputs, block_valid_1, (block_invalid_2,False) ]
    }

def gen_test_tx_early_recursive():
    description = "Block with early tx check, recursive (block in txids)"
    block_valid_1 = mkBlock(None, [coinbase_trans], description)
    mine(block_valid_1)
    transfer_valid_inputs = mkTrans([transIn(0, coinbase_trans),transIn(1,"000d2a956862efbb621977bb9757e3ed5c95cb715fe0d79067fd301ea9dfb39c")],[transOut(1,50000)])
    full_signature (0, transfer_valid_inputs)
    block_invalid_2 = mkBlock(block_valid_1, [transfer_valid_inputs,block_valid_1], description)
    mine(block_invalid_2)
    coinbase_trans_3 = mkCoinbase(0, 3)
    block_valid_3 = mkBlock(block_invalid_2, [coinbase_trans_3], description)
    return {
            'description': description,
            'expected': 'INVALID_ANCESTRY',
            'objects': [ coinbase_trans, transfer_valid_inputs, coinbase_trans_3, block_valid_1, block_invalid_2, (block_valid_3,False) ]
    }

def gen_test_tx_early_sig_check_recursive():
    description = "Block with early signature check, recursive"
    transfer_invalid_sig = mkTrans([transIn(0, coinbase_trans),transIn(1,"000d2a956862efbb621977bb9757e3ed5c95cb715fe0d79067fd301ea9dfb39c")],[transOut(1,50000)])
    full_signature (0, transfer_invalid_sig)
    transfer_invalid_sig['object']['inputs'][0]['sig'] = "000d2a956862efbb621977bb9757e3ed5c95cb715fe0d79067fd301ea9dfb39c000d2a956862efbb621977bb9757e3ed5c95cb715fe0d79067fd301ea9dfb39c"
    block_invalid_1 = mkBlock(None, [transfer_invalid_sig], description)
    mine(block_invalid_1)
    cb1 = mkCoinbase(0, 3)
    block_valid_2 = mkBlock(block_invalid_1, [cb1], description)
    return {
            'description': description,
            'expected': 'INVALID_ANCESTRY',
            'objects': [ coinbase_trans, cb1, transfer_invalid_sig, (block_valid_2,False), block_invalid_1 ]
    }

