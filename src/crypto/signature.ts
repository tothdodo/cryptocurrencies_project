import { verify } from "@noble/ed25519";

export type PublicKey = string
export type Signature = string

/**
 * returns true iff the given signature is valid
 * @param sig a signature to check 
 * @param message the message that was signed
 * @param pubkey the public key under which the signature should be verified
 */

export async function ver(sig: Signature, message: string, pubkey: PublicKey): Promise<boolean> {
  // Convert inputs to Uint8Array to satisfy @noble/ed25519 typings
  const sigBytes = Uint8Array.from(Buffer.from(sig, 'hex'));
  const pubkeyBytes = Uint8Array.from(Buffer.from(pubkey, 'hex'));
  const messageBytes = new TextEncoder().encode(message);
  return await verify(sigBytes, messageBytes, pubkeyBytes);
}
