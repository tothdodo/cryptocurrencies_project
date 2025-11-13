import { ObjectId, objectManager } from './object'
import {
  TransactionInputObjectType,
  TransactionObjectType,
  TransactionOutputObjectType,
  OutpointObjectType,
  SpendingTransactionObject,
  TransactionOutputObject
} from './message'
import { PublicKey, Signature } from './crypto/signature'
import { canonicalize } from 'json-canonicalize'
import { ver } from './crypto/signature'
import { logger } from './logger'
import { Block } from './block'
import { INVALID_ANCESTRY, INVALID_FORMAT, INVALID_TX_CONSERVATION, INVALID_TX_OUTPOINT, INVALID_TX_SIGNATURE, Peer, UNKNOWN_OBJECT } from './peer'

/**
 * a class to represent a transaction output
 */
export class Output {
  publickey: PublicKey
  value: number

  static fromNetworkObject(outputMsg: TransactionOutputObjectType): Output {
    const output = new Output(outputMsg.pubkey, outputMsg.value);
    return output;
  }

  constructor(pubkey: PublicKey, value: number) {
    this.publickey = pubkey;
    this.value = value;
  }

  toNetworkObject(): TransactionOutputObjectType {
    return {
      'pubkey': this.publickey,
      'value': this.value
    };
  }
}

/**
 * a class to represent a transaction outpoint
 */
export class Outpoint {
  txid: ObjectId
  index: number

  constructor(txid: ObjectId, index: number) {
    this.txid = txid;
    this.index = index;
  }

  /**
   * Gets the output referenced by this outpoint
   * @returns the referenced output
   */
  async resolve(peer: Peer): Promise<Output> {
    const outpointedTx = await objectManager.get(this.txid);
    if (outpointedTx === null) {
      peer?.fatalError(`The referenced transaction ${this.txid} does not exist in the database.`, UNKNOWN_OBJECT)
      throw new Error();
    }
    if (outpointedTx.type === "block") {
      peer?.fatalError(`An object with id ${this.txid} exists but is a block `, INVALID_FORMAT);
      throw new Error();
    }
    if (outpointedTx.outputs.length <= this.index || this.index < 0) {
      peer?.fatalError(`The referenced transaction ${this.txid} has no output at index ${this.index}.`, INVALID_TX_OUTPOINT)
      throw new Error();
    }
    if (!await objectManager.validate(outpointedTx, peer)) {
      peer?.fatalError(`The referenced transaction ${this.txid} is invalid.`, INVALID_ANCESTRY)
      throw new Error();
    }
    const output = outpointedTx.outputs[this.index];
    return new Output(output.pubkey, output.value);
  }

  toNetworkObject(): OutpointObjectType {
    return {
      'txid': this.txid,
      'index': this.index
    };
  }

  toString() {
    return canonicalize(this.toNetworkObject());
  }
}

export class Input {
  outpoint: Outpoint
  signature: Signature | null

  static fromNetworkObject(inputMsg: TransactionInputObjectType): Input {
    const outpoint = new Outpoint(inputMsg.outpoint.txid, inputMsg.outpoint.index);
    const signature = inputMsg.sig ?? null;
    return new Input(outpoint, signature);
  }
  constructor(outpoint: Outpoint, signature: Signature | null) {
    this.outpoint = outpoint;
    this.signature = signature;
  }

  toNetworkObject(): TransactionInputObjectType {
    return {
      'outpoint': this.outpoint.toNetworkObject(),
      'sig': this.signature
    };
  }

  /**
   * @returns this input without a signature
   */
  toUnsigned(): Input {
    return new Input(this.outpoint, null);
  }
}

/**
 * a class to represent transactions
 */
export class Transaction {
  outputs: Output[]
  inputs?: Input[] // only for spending transactions
  height?: number // only for coinbase transactions

  static inputsFromNetworkObject(inputMsgs: TransactionInputObjectType[]) {
    return inputMsgs.map(inputMsg => Input.fromNetworkObject(inputMsg));
  }
  static outputsFromNetworkObject(outputMsgs: TransactionOutputObjectType[]) {
    return outputMsgs.map(outputMsg => Output.fromNetworkObject(outputMsg));
  }
  static fromNetworkObject(txObj: TransactionObjectType): Transaction {
    if ('height' in txObj) {
      const outputs = this.outputsFromNetworkObject(txObj.outputs);
      const tx = new Transaction(outputs, undefined, txObj.height);
      return tx;
    }
    const inputs = this.inputsFromNetworkObject(txObj.inputs);
    const outputs = this.outputsFromNetworkObject(txObj.outputs);
    return new Transaction(outputs, inputs);
  }
  static async byId(txid: ObjectId): Promise<Transaction> {
    const txObj = await objectManager.get(txid) as TransactionObjectType;
    return this.fromNetworkObject(txObj);
  }
  constructor(outputs: Output[], inputs?: Input[], height?: number) {
    this.outputs = outputs;
    this.inputs = inputs;
    this.height = height;
  }

  isCoinbase(): Boolean {
    return this.inputs === undefined && typeof this.height === 'number';
  }
  async validate(peer: Peer, idx?: number, block?: Block): Promise<Boolean> {
    // validate 0: assume coinbase transactions are always valid
    if (this.isCoinbase()) {
      return true;
    }
    let inputSum: number = 0;
    for (let input of this.inputs!) {
      try {
        // validate 1: verify that the referenced output exists
        const resolvedOutput = await input.outpoint.resolve(peer);
        if (input.signature === null) {
          peer?.fatalError("Signature is null", INVALID_TX_SIGNATURE)
          return false;
        }
        // validate 2: verify the signature
        // An input contains a pointer to a previous output in the outpoint key and a signature in the
        // sig key. The outpoint key contains a dictionary of two keys: txid and index. The txid is
        // the objectid of the previous transaction, while the index is the natural number (zero-based)
        // indexing an output within that transaction. The sig key contains the signature.
        const sigVerified = await ver(input.signature, this.toString(), resolvedOutput.publickey)
        if (!sigVerified) {
          peer?.fatalError("Verifying the signature has failed", INVALID_TX_SIGNATURE)
          return false;
        }
        inputSum += resolvedOutput.value;
      } catch (error) {
        console.log(error)
        return false;
      }
    }
    // validate 3: outputs validation
    // Outputs contain a public key and a value. The public keys must be in the correct
    // format and the values must be a non-negative integer.
    try {
      for (let output of this.outputs) {
        const networkOutput: TransactionOutputObjectType = output.toNetworkObject();
        TransactionOutputObject.check(networkOutput);
      }
    } catch (error) {
      peer?.fatalError("Output key formats are not valid", INVALID_FORMAT)
      return false;
    }
    // validate 4: verify input/output value balance
    // Transactions must satisfy the weak law of conservation: The sum of input values must be
    // equal or exceed the sum of output values. Any remaining value can be collected as fees by
    // the miner confirming the transaction.
    const outputSum = this.outputs.reduce((sum, output) => sum + output.value, 0);
    if (inputSum < outputSum) {
      peer?.fatalError(`The output(s) sum in the referenced transaction(s) hold(s) less than ${outputSum} picaker`, INVALID_TX_CONSERVATION)
      return false;
    }
    return true;
  }

  inputsUnsigned() {
    if (!this.inputs) {
      return undefined;
    }
    return this.inputs.map(input => input.toUnsigned());
  }
  toNetworkObject(signed: boolean = true): TransactionObjectType {
    return this.isCoinbase() ? {
      'type': 'transaction',
      'height': this.height!,
      'outputs': this.outputs.map(output => output.toNetworkObject())
    } : {
      'type': 'transaction',
      'inputs': this.inputs!.map(input => signed ? input.toNetworkObject() : input.toUnsigned().toNetworkObject()),
      'outputs': this.outputs.map(output => output.toNetworkObject())
    };
  }
  toString() {
    return canonicalize(this.toNetworkObject());
  }
}
