import {
  BlockObject, BlockObjectType,
  TransactionObject, ObjectType,
  UNFINDABLE_OBJECT,
  INVALID_FORMAT,
  INVALID_BLOCK_POW
} from './message'
import { hash } from './crypto/hash'
import { canonicalize } from 'json-canonicalize'
import { Peer } from './peer'
import { objectManager, ObjectId, db } from './object'
import { UTXOSet } from './utxo'
import { logger } from './logger'
import { Transaction } from './transaction'
import { chainManager } from './chain'
import { Deferred } from './promise'
import { Static, String } from "runtypes";
import { CustomError } from './errors'

const TARGET = '0' /* TODO */
const GENESIS: BlockObjectType = {
  "T": "00000000abc00000000000000000000000000000000000000000000000000000",
  "created": 1671062400,
  "miner": "Marabu",
  "nonce": "000000000000000000000000000000000000000000000000000000021bea03ed",
  "note": "The New York Times 2022-12-13: Scientists Achieve Nuclear Fusion Breakthrough With Blast of 192 Lasers",
  "previd": null,
  "txids": [],
  "type": "block"
}
const BU = 10 ** 12
const BLOCK_REWARD = 50 * BU

const Hex32 = String.withConstraint(
  (str) =>
    /^[0-9a-fA-F]{64}$/.test(str) ||
    'Invalid hex: must be a 32-byte (64 hex chars) hexadecimal string'
);
type Hex32Type = Static<typeof Hex32>

// ASCII-printable string up to 128 chars
const AsciiPrintable128 = String.withConstraint(
  (str) =>
    /^[\x20-\x7E]{0,128}$/.test(str) ||
    'Invalid string: must be ASCII-printable and ≤ 128 chars'
);

type AsciiPrintableType128 = Static<typeof AsciiPrintable128>

export class BlockManager {
  blocks: Map<string, Block>;

  constructor() {
    this.blocks = new Map();
  }
  async exists(blockid: ObjectId) {
    return await db.exists(blockid)
  }

  async get(blockid: ObjectId) {
    return await db.get(blockid)
  }

  async del(blockid: ObjectId) {
    this.blocks.delete(blockid);
    return await db.del(blockid)
  }

  async put(block: Block) {
    this.blocks.set(block.blockid, block);
    return await db.put(block.blockid, block)
  }
}

export const blockManager = new BlockManager()

/**
 * Class used to represent a block
 */
export class Block {
  /* TODO */
  blockid: ObjectId;
  txids: ObjectId[];
  nonce: Hex32Type;
  previd: ObjectId | null;
  created: number;
  T: Hex32Type;

  miner: AsciiPrintableType128;
  note: AsciiPrintableType128;

  utxo: UTXOSet;

  /**
   * Builds a Block object from GENESIS
   * @returns the genesis block
   */
  public static async makeGenesis(): Promise<Block> {
    return Block.fromNetworkObject(GENESIS);
  }

  /**
   * Builds a block object from given BlockObject collection
   * @param object 
   * @returns a Block object representing this block
   */
  public static fromNetworkObject(object: BlockObjectType): Block {
    return new Block(object);
  }

  constructor(
    block: BlockObjectType
  ) {
    this.blockid = objectManager.id(block);
    this.txids = block.txids;
    this.nonce = block.nonce;
    this.previd = block.previd;
    this.created = block.created;
    this.T = block.T;
    this.miner = block.miner ?? "";
    this.note = block.note ?? "";
    this.utxo = new UTXOSet(new Set<string>());
  }

  /**
   * Attempts to fetch the coinbase transaction from this block, throws an Error if not present
   * @returns the coinbase transaction, if present
   * @throws Error
   */
  async getCoinbase(): Promise<Transaction> {
    /* TODO */
    return new Transaction("d46d09138f0251edc32e28f1a744cb0b7286850e4c9c777d7e3c6e459b289347", [], [], null); // TODO: change
  }

  hasPoW(): boolean {
    const blockIdBigInt = BigInt("0x" + this.blockid);
    const targetBigInt = BigInt("0x" + this.T);

    return blockIdBigInt < targetBigInt;
  }

  isGenesis(): boolean {
    return this.previd === null;
  }

  /**
   * Attempts to get all transaction objects from their IDs referenced in this block, throws an Error if not all could be loaded
   * @returns collecetion of transaction
   * @throws Error
   */
  async getTxs(): Promise<Transaction[]> {
    const txs: Transaction[] = [];
    const missingTXIDs: Set<string> = new Set<string>();
    for (let i = 0; i < this.txids.length; i++) {
      const txid = this.txids[i];
      try {
        const tx = await Transaction.byId(txid);
        txs.push(tx);
      } catch (e) {
        missingTXIDs.add(txid);
      }
    }
    if (missingTXIDs.size > 0) {
      throw new CustomError(
        `Some transactions referenced in block ${this.blockid} could not be found`,
        UNFINDABLE_OBJECT,
        true,
        missingTXIDs
      );
    }

    return txs;
  }

  /**
   * Validates a transaction, throws an Error if transaction failed to verify
   * @throws Error
   */
  async validateTx(tx: Transaction, index: number) {
    try {
      await tx.validate();
    } catch (e) {
      throw e;
    }
  }

  /**
   * Gets the parent block, returning null on failure
   * @returns Block
   */
  async loadParent(): Promise<Block | null> {
    const parentId = this.previd;
    if (parentId !== null) {
      try {
        return await objectManager.get(parentId);
      } catch (e) {
        return null;
      }
    }
    return null;
  }

  /**
   * Validates the ancestry of this block until a block that has already been verified is hit
   * @returns parent Block if valid, otherwise null
   */
  async validateAncestry(/* TODO */): Promise<Block | null> {
    /* TODO */
    return null;
  }

  /**
   * Validate this block, throwing an error if validation failed
   * @throws Error
   */
  async validate(startValidationFromTXIdx: string = "") {
    if (startValidationFromTXIdx === "") {
      // Validate fields
      if (
        !this ||
        !("blockid" in this) ||
        !("T" in this) ||
        !("created" in this) ||
        !("nonce" in this) ||
        !("previd" in this) ||
        !("txids" in this) ||
        !("note" in this) ||
        !("miner" in this) ||
        !Hex32.check(this.T) ||
        typeof this.created !== "number" ||
        !AsciiPrintable128.check(this.miner) ||
        !AsciiPrintable128.check(this.note) ||
        !Hex32.check(this.nonce) ||
        (this.previd !== null && !Hex32.check(this.previd)) ||
        !Array.isArray(this.txids) ||
        this.txids.some((id: any) => !Hex32.check(id))
      ) {
        throw new CustomError(`Invalid block fields: ${this.T}`, INVALID_FORMAT);
      }

      // Validate target
      if (this.T !== "0000abc000000000000000000000000000000000000000000000000000000000") {
        throw new CustomError(`Invalid block target: ${this.T}`, INVALID_FORMAT);
      }

      // Validate proof-of-work
      if (!this.hasPoW()) {
        throw new CustomError(`Block ${this.blockid} does not satisfy proof-of-work requirement`, INVALID_BLOCK_POW);
      }
    }

    let txs: Transaction[];
    try {
      txs = await this.getTxs();
    } catch (e) {
      throw e;
    }

    try {
      txs.forEach(async (tx, index) => {
        await this.validateTx(tx, index);
      });
    } catch (e) {
      throw e;
    }
  }

  /**
   * save this block (alongside meta information) in the database
   */
  async save() {
    await blockManager.put(this);
  }

  /**
   * load this block data and meta information
   */
  async load(blockid: string): Promise<Block | null> {
    const data = await blockManager.get(blockid)
    if (!data) return null

    const utxo = new UTXOSet(new Set(data.utxo))
    const block = Block.fromNetworkObject(data.block)
    block.utxo = utxo
    return block
  }
}
