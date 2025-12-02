import { Request, Response, NextFunction } from "express";
import { CONFIG } from "../config/constants.js";

// Simple in-memory rate limiter
// LIMITATION: This will not scale across multiple instances and will reset on restart
// For production with multiple instances, use Redis-backed rate limiting:
// - npm install express-rate-limit rate-limit-redis
// - Configure with Redis connection from environment
const requestCounts = new Map<string, { count: number; resetTime: number }>();

export function rateLimiter(req: Request, res: Response, next: NextFunction) {
  const identifier = req.ip || req.socket.remoteAddress || "unknown";
  const now = Date.now();

  const record = requestCounts.get(identifier);

  if (!record || now > record.resetTime) {
    // New window
    requestCounts.set(identifier, {
      count: 1,
      resetTime: now + CONFIG.RATE_LIMIT_WINDOW_MS
    });
    return next();
  }

  if (record.count >= CONFIG.RATE_LIMIT_MAX_REQUESTS) {
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
