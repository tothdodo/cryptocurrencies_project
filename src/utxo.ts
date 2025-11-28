import { Block } from './block'
import { CustomError } from './errors'
import { logger } from './logger'
import { INVALID_TX_CONSERVATION, OutpointObject, OutpointObjectType } from './message'
import { db, ObjectId } from './object'
import { Outpoint, Transaction } from './transaction'

export type UTXO = Set<string>

/**
 * a class to represent the UTXO (unspent transaction output) set
 */

export class UTXOSet {
  set: UTXO

  constructor(outpoints: UTXO) {
    this.set = new Set(outpoints)
  }

  copy(): UTXOSet {
    return new UTXOSet(new Set(this.set))
  }

  /**
   * Applies the transaction on the current utxo set, throwing an error if this is not possible
   * @param tx 
   * @throws Error
   */
  async apply(tx: Transaction) {
    // --- 1. CHECK INPUTS EXIST ---
    for (const input of tx.inputs) {
      const key = `${input.outpoint.txid}:${input.outpoint.index}`

      if (!this.set.has(key)) {
        throw new CustomError(
          `Transaction ${tx.txid} tries to spend missing UTXO ${key}`,
          INVALID_TX_CONSERVATION
        );
      }
    }

    // --- 2. REMOVE SPENT OUTPUTS ---
    for (const input of tx.inputs) {
      const key = `${input.outpoint.txid}:${input.outpoint.index}`
      this.set.delete(key)
    }

    // --- 3. ADD NEW OUTPUTS ---
    tx.outputs.forEach((_, index) => {
      const key = `${tx.txid}:${index}`
      this.set.add(key)
    })
  }

  /**
   * Applies multiple transaction to the current utxo set
   * @throws Error
   */
  async applyMultiple(txs: Transaction[]) {
    for (const tx of txs) {
      await this.apply(tx)
    }
  }

  toString() {
    return `UTXOSet(${Array.from(this.set).join(', ')})`
  }
}
