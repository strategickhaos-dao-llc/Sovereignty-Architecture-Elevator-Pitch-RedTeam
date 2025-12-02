import { Request, Response, NextFunction } from "express";
import { db } from "../db.js";
import { AuthRequest } from "./auth.js";

export async function auditLogger(req: AuthRequest, res: Response, next: NextFunction) {
  // Only log API calls, not static assets
  if (!req.path.startsWith("/api/")) {
    return next();
  }

  const originalSend = res.send;
  const startTime = Date.now();

  res.send = function (data: any) {
    res.send = originalSend;

    // Log after response is sent
    const duration = Date.now() - startTime;
    
    // Only log if user is authenticated or it's an auth endpoint
    if (req.user || req.path.startsWith("/api/auth/")) {
      logAudit(req, res.statusCode, duration).catch(err => 
        console.error("Audit logging error:", err)
      );
    }

    return originalSend.call(this, data);
  };

  next();
}

async function logAudit(req: AuthRequest, statusCode: number, duration: number) {
  try {
    const action = `${req.method} ${req.path}`;
    const userId = req.user?.id || null;
    const ipAddress = req.ip || req.socket.remoteAddress;
    const userAgent = req.get("user-agent");

    await db.query(
      `INSERT INTO audit_log (user_id, action, resource, details, ip_address, user_agent)
       VALUES ($1, $2, $3, $4, $5, $6)`,
      [
        userId,
        action,
        req.originalUrl,
        JSON.stringify({
          statusCode,
          duration,
          body: req.body && Object.keys(req.body).length > 0 ? sanitizeBody(req.body) : null
        }),
        ipAddress,
        userAgent
      ]
    );
  } catch (error) {
    console.error("Failed to write audit log:", error);
  }
}

function sanitizeBody(body: any): any {
  // Remove sensitive fields from audit log
  const sanitized = { ...body };
  const sensitiveFields = ["password", "token", "secret", "apiKey"];
  
  for (const field of sensitiveFields) {
    if (sanitized[field]) {
      sanitized[field] = "[REDACTED]";
    }
  }
  
  return sanitized;
}
