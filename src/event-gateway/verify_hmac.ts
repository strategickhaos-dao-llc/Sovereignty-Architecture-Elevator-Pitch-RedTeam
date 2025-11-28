// Minimal HMAC + replay protection middleware for Node/Express (TypeScript)
// Supports optional Redis for replay cache; falls back to in-memory TTL cache.
// Usage: app.post('/webhook', verifyHmac({ secretResolver, redisClient }), handler)

import crypto from "crypto";
import { Request, Response, NextFunction } from "express";
import type { Redis } from "ioredis";

type SecretResolver = (version: string | null, req: Request) => Promise<string | null>;

interface Options {
  secretResolver: SecretResolver; // returns secret for given version (or null)
  headerName?: string; // header containing signature (default: x-hub-signature-256)
  algorithm?: string; // default: sha256
  replayTtlSeconds?: number; // default: 300
  redisClient?: Redis; // optional Redis instance for replay cache
  nonceHeader?: string; // header that contains nonce (default: x-event-nonce)
  versionHeader?: string; // header that contains secret version (default: x-signature-version)
}

const DEFAULTS = {
  headerName: "x-hub-signature-256",
  algorithm: "sha256",
  replayTtlSeconds: 300,
  nonceHeader: "x-event-nonce",
  versionHeader: "x-signature-version",
};

const inMemoryCache = new Map<string, number>();

export function verifyHmac(opts: Options) {
  const headerName = opts.headerName ?? DEFAULTS.headerName;
  const algorithm = opts.algorithm ?? DEFAULTS.algorithm;
  const ttl = opts.replayTtlSeconds ?? DEFAULTS.replayTtlSeconds;
  const nonceHeader = opts.nonceHeader ?? DEFAULTS.nonceHeader;
  const versionHeader = opts.versionHeader ?? DEFAULTS.versionHeader;
  const redis = opts.redisClient;

  // prune in-memory cache periodically
  setInterval(() => {
    const now = Date.now();
    for (const [k, v] of Array.from(inMemoryCache)) {
      if (v < now) inMemoryCache.delete(k);
    }
  }, 60_000).unref();

  return async function (req: Request, res: Response, next: NextFunction) {
    try {
      const sigHeader = req.header(headerName);
      if (!sigHeader) return res.status(400).send("Missing signature header");

      // Expect format: sha256=base16sig or versioned formats are resolved by version header
      const version = req.header(versionHeader) ?? null;
      const secret = await opts.secretResolver(version, req);
      if (!secret) return res.status(401).send("Unknown signature version");

      // Read raw body for exact HMAC calculation. Expect middleware (raw body) to have preserved it.
      // For express, ensure app.use(express.raw({ type: '*/*' })) for webhook routes.
      const raw = (req as any).rawBody as Buffer | undefined;
      if (!raw) return res.status(500).send("Server misconfiguration: raw body required");

      const computed = crypto.createHmac(algorithm, secret).update(raw).digest("hex");
      const expected = sigHeader.startsWith(`${algorithm}=`) ? sigHeader.split("=")[1] : sigHeader;

      // Constant-time comparison that handles different lengths safely
      // Pad shorter buffer to match longer one to prevent timing attacks from length checks
      const computedBuf = Buffer.from(computed);
      const expectedBuf = Buffer.from(expected);
      const maxLen = Math.max(computedBuf.length, expectedBuf.length);
      
      // Pad both buffers to the same length with zeros for constant-time comparison
      const paddedComputed = Buffer.concat([computedBuf], maxLen);
      const paddedExpected = Buffer.concat([expectedBuf], maxLen);
      
      // Perform constant-time comparison, but also track if lengths were different
      const lengthMatch = computedBuf.length === expectedBuf.length;
      const contentMatch = crypto.timingSafeEqual(paddedComputed, paddedExpected);
      
      // Both length and content must match
      if (!lengthMatch || !contentMatch) {
        return res.status(401).send("Invalid signature");
      }

      // Replay protection: require nonce header
      const nonce = req.header(nonceHeader) ?? null;
      if (!nonce) return res.status(400).send("Missing nonce for replay protection");

      const key = `replay:${version ?? "v0"}:${nonce}`;

      if (redis) {
        const added = await redis.setnx(key, "1");
        if (!added) return res.status(409).send("Replay detected");
        await redis.expire(key, ttl);
      } else {
        const now = Date.now();
        const until = now + ttl * 1000;
        if (inMemoryCache.has(key)) return res.status(409).send("Replay detected");
        inMemoryCache.set(key, until);
      }

      // Passed HMAC and replay checks
      return next();
    } catch (err) {
      // don't leak secrets in errors
      console.error("verifyHmac error:", (err as Error).message);
      return res.status(500).send("HMAC verification error");
    }
  };
}
