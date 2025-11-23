import { Request, Response, NextFunction } from "express";

// Simple in-memory rate limiter
// For production, use Redis-backed rate limiter
const requestCounts = new Map<string, { count: number; resetTime: number }>();

const RATE_LIMIT = 100; // requests per window
const WINDOW_MS = 15 * 60 * 1000; // 15 minutes

export function rateLimiter(req: Request, res: Response, next: NextFunction) {
  const identifier = req.ip || req.socket.remoteAddress || "unknown";
  const now = Date.now();

  const record = requestCounts.get(identifier);

  if (!record || now > record.resetTime) {
    // New window
    requestCounts.set(identifier, {
      count: 1,
      resetTime: now + WINDOW_MS
    });
    return next();
  }

  if (record.count >= RATE_LIMIT) {
    return res.status(429).json({
      error: "Too many requests",
      retryAfter: Math.ceil((record.resetTime - now) / 1000)
    });
  }

  record.count++;
  next();
}

// Cleanup old entries every hour
setInterval(() => {
  const now = Date.now();
  for (const [key, value] of requestCounts.entries()) {
    if (now > value.resetTime) {
      requestCounts.delete(key);
    }
  }
}, 60 * 60 * 1000);
