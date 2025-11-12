export type ObjectId = string

import level from 'level-ts'
import { canonicalize } from 'json-canonicalize'
import {
  Object, ObjectType,
  TransactionObjectType, BlockObjectType
} from './message'
import { Transaction } from './transaction'
import { Block } from './block'
import { logger } from './logger'
import { hash, normalize } from './crypto/hash'
import { Peer } from './peer'
import { Deferred, delay, resolveToReject } from './promise'
import { mempool } from './mempool'

export const db = new level('./db')
const OBJECT_AVAILABILITY_TIMEOUT = 5000 // ms

/**
 * Interfaces the database
 */
class ObjectManager {
  /* TODO */
  knownObjectIds: Set<ObjectId> = new Set()

  id(obj: any) {
    const normalized = normalize(obj)
    return hash(canonicalize(normalized))
  }

  /**
   * Checks if you know about this object
   * @param objectid 
   */
  async exists(objectid: ObjectId) {
    return await db.exists(objectid)
  }

  async get(objectid: ObjectId) {
    try {
      return await db.get(objectid)
    } catch {
      return null;
    }
  }

  async getAll(): Promise<Record<string, ObjectType>> {
    const entries = await db.stream({ keys: true, values: true });
    const result: Record<string, ObjectType> = {};

    for (const { key, value } of entries) {
      result[key] = value;
    }

    return result;
  }


  async del(objectid: ObjectId) {
    await db.del(objectid)
    this.knownObjectIds.delete(objectid)
  }

  async put(object: any) {
    const id = this.id(object.object)
    await db.put(id, normalize(object.object))
    this.knownObjectIds.add(id)
  }

  async putTest(id: string, object: ObjectType) {
    await db.put(id, object);
    this.knownObjectIds.add(this.id(object))
  }

  // IMPORTANT
  // VISSZA peer?: Peer ÉS peer!
  // IMPORTANT
  async validate(object: ObjectType, peer?: Peer): Promise<Boolean> {
    /* TODO */
    if (object.type === 'transaction') {
      const tx = Transaction.fromNetworkObject(object as TransactionObjectType);
      return tx.validate(peer!);
    }
    if (object.type === 'block') {
      const block = await Block.fromNetworkObject(object as BlockObjectType);
      return block.validate();
    }
    return false;
  }

  /**
   * Attempts to retrieve an object from a peer
   * @param objectid the object to get
   * @param peer the peer you want to get the object from
   * @returns the object, or rejects if not possible
   */
  async retrieve(objectid: ObjectId, peer: Peer): Promise<void> { // todo: Promise<ObjectType>
    /* TODO */
    const alreadyHave = await this.exists(objectid);
    if (alreadyHave) {
      return; // placeholder
    }


  }
}

export const objectManager = new ObjectManager()
