import crypto from "crypto";

/**
 * HMAC Verification with Replay Protection
 * Strategickhaos DAO LLC - Event Gateway Security
 * 
 * Features:
 * - HMAC-SHA256 signature verification
 * - Replay attack protection via nonce + TTL
 * - In-memory cache with automatic expiration
 */

interface NonceEntry {
  timestamp: number;
}

// In-memory replay cache (use Redis for distributed deployments)
const nonceCache = new Map<string, NonceEntry>();

// Configuration
const NONCE_TTL_MS = 5 * 60 * 1000; // 5 minutes TTL for replay protection
const MAX_TIMESTAMP_DRIFT_MS = 60 * 1000; // Allow 60 seconds timestamp drift
const CLEANUP_INTERVAL_MS = 60 * 1000; // Clean expired nonces every minute

// Start cleanup interval
let cleanupInterval: NodeJS.Timeout | null = null;

/**
 * Initialize the replay protection cache cleanup
 */
export function initReplayProtection(): void {
  if (cleanupInterval) return;
  cleanupInterval = setInterval(() => {
    const now = Date.now();
    for (const [nonce, entry] of nonceCache.entries()) {
      if (now - entry.timestamp > NONCE_TTL_MS) {
        nonceCache.delete(nonce);
      }
    }
  }, CLEANUP_INTERVAL_MS);
}

/**
 * Stop the replay protection cleanup interval
 */
export function stopReplayProtection(): void {
  if (cleanupInterval) {
    clearInterval(cleanupInterval);
    cleanupInterval = null;
  }
}

/**
 * Verify HMAC signature with timing-safe comparison
 * @param secret - The HMAC secret key
 * @param payload - The raw request payload
 * @param signature - The signature from the request header
 * @param algorithm - Hash algorithm (default: sha256)
 * @returns true if signature is valid
 */
export function verifyHmacSignature(
  secret: string,
  payload: string | Buffer,
  signature: string,
  algorithm: string = "sha256"
): boolean {
  if (!secret || !payload || !signature) {
    return false;
  }

  try {
    const expectedSig = crypto
      .createHmac(algorithm, secret)
      .update(payload)
      .digest("hex");

    // Support both raw and prefixed signatures
    const normalizedSig = signature.startsWith(`${algorithm}=`)
      ? signature.slice(algorithm.length + 1)
      : signature;

    // Timing-safe comparison
    const expectedBuffer = Buffer.from(expectedSig, "hex");
    const actualBuffer = Buffer.from(normalizedSig, "hex");

    if (expectedBuffer.length !== actualBuffer.length) {
      return false;
    }

    return crypto.timingSafeEqual(expectedBuffer, actualBuffer);
  } catch {
    return false;
  }
}

/**
 * Verify request timestamp is within acceptable drift
 * @param timestamp - ISO 8601 timestamp from request
 * @returns true if timestamp is valid and within drift window
 */
export function verifyTimestamp(timestamp: string | number): boolean {
  if (!timestamp) return false;

  try {
    const requestTime = typeof timestamp === "number" 
      ? timestamp 
      : new Date(timestamp).getTime();
    const now = Date.now();
    const drift = Math.abs(now - requestTime);

    return drift <= MAX_TIMESTAMP_DRIFT_MS;
  } catch {
    return false;
  }
}

/**
 * Check if nonce has been used (replay attack prevention)
 * @param nonce - Unique request identifier
 * @returns true if nonce is unique (not a replay)
 */
export function checkNonce(nonce: string): boolean {
  if (!nonce) return false;

  // Check if nonce exists in cache
  if (nonceCache.has(nonce)) {
    return false; // Replay detected
  }

  // Store nonce with current timestamp
  nonceCache.set(nonce, { timestamp: Date.now() });
  return true;
}

/**
 * Comprehensive webhook verification
 * Verifies HMAC signature, timestamp, and nonce for full replay protection
 */
export interface VerifyWebhookOptions {
  secret: string;
  payload: string | Buffer;
  signature: string;
  timestamp?: string | number;
  nonce?: string;
  algorithm?: string;
}

export interface VerifyResult {
  valid: boolean;
  error?: string;
}

export function verifyWebhook(options: VerifyWebhookOptions): VerifyResult {
  const { secret, payload, signature, timestamp, nonce, algorithm = "sha256" } = options;

  // Verify HMAC signature
  if (!verifyHmacSignature(secret, payload, signature, algorithm)) {
    return { valid: false, error: "Invalid HMAC signature" };
  }

  // Verify timestamp if provided
  if (timestamp !== undefined && !verifyTimestamp(timestamp)) {
    return { valid: false, error: "Request timestamp out of valid range" };
  }

  // Check nonce for replay protection if provided
  if (nonce !== undefined && !checkNonce(nonce)) {
    return { valid: false, error: "Duplicate nonce detected (possible replay attack)" };
  }

  return { valid: true };
}

/**
 * Express middleware for webhook HMAC verification
 */
export function createHmacMiddleware(config: {
  secretEnvVar: string;
  signatureHeader: string;
  timestampHeader?: string;
  nonceHeader?: string;
  algorithm?: string;
}) {
  return (req: any, res: any, next: any) => {
    const secret = process.env[config.secretEnvVar];
    if (!secret) {
      console.error(`Missing ${config.secretEnvVar} environment variable`);
      return res.status(500).json({ error: "Server configuration error" });
    }

    const signature = req.get(config.signatureHeader) || "";
    const timestamp = config.timestampHeader ? req.get(config.timestampHeader) : undefined;
    const nonce = config.nonceHeader ? req.get(config.nonceHeader) : undefined;
    const payload = req.rawBody || "";

    const result = verifyWebhook({
      secret,
      payload,
      signature,
      timestamp,
      nonce,
      algorithm: config.algorithm
    });

    if (!result.valid) {
      console.warn(`Webhook verification failed: ${result.error}`);
      return res.status(401).json({ error: result.error });
    }

    next();
  };
}

// Initialize replay protection on module load
initReplayProtection();
