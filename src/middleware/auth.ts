import { Request, Response, NextFunction } from "express";
import { db } from "../db.js";

export interface AuthRequest extends Request {
  user?: {
    id: number;
    email: string;
    username: string;
    role: string;
  };
}

export async function requireAuth(req: AuthRequest, res: Response, next: NextFunction) {
  const sessionToken = req.session?.userId;

  if (!sessionToken) {
    return res.status(401).json({ error: "Authentication required" });
  }

  try {
    // Verify session and get user
    const result = await db.query(
      `SELECT u.id, u.email, u.username, u.role, u.is_active
       FROM users u
       WHERE u.id = $1 AND u.is_active = true`,
      [sessionToken]
    );

    if (result.rows.length === 0) {
      req.session.destroy(() => {});
      return res.status(401).json({ error: "Invalid session" });
    }

    req.user = result.rows[0];
    next();
  } catch (error) {
    console.error("Auth middleware error:", error);
    return res.status(500).json({ error: "Authentication error" });
  }
}

export function requireRole(role: string) {
  return (req: AuthRequest, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: "Authentication required" });
    }

    if (req.user.role !== role && req.user.role !== "admin") {
      return res.status(403).json({ error: "Insufficient permissions" });
    }

    next();
  };
}
