import crypto from 'crypto';

/**
 * returns the hash of given string
 * @param str 
 */
export function hash(str: string): string {
  const hash = crypto.createHash('blake2s256').update(str).digest();
  return hash.toString('hex');
}

export function normalize(obj: any): any {
  if (Array.isArray(obj)) return obj.map(normalize);

  if (obj && typeof obj === 'object') {
    return Object.fromEntries(
      Object.entries(obj).map(([k, v]) => [k.trim(), normalize(v)])
    );
  }

  if (typeof obj === 'string') return obj.trim();

  return obj;
}

