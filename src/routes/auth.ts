import express from "express";
import bcrypt from "bcrypt";
import { randomBytes } from "crypto";
import { db } from "../db.js";
import { CONFIG } from "../config/constants.js";

export const authRouter = express.Router();

// Login endpoint
authRouter.post("/login", async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: "Email and password required" });
  }

  try {
    const result = await db.query(
      "SELECT id, email, username, password_hash, role, is_active FROM users WHERE email = $1",
      [email]
    );

    if (result.rows.length === 0) {
      return res.status(401).json({ error: "Invalid credentials" });
    }

    const user = result.rows[0];

    if (!user.is_active) {
      return res.status(403).json({ error: "Account is inactive" });
    }

    const passwordMatch = await bcrypt.compare(password, user.password_hash);

    if (!passwordMatch) {
      return res.status(401).json({ error: "Invalid credentials" });
    }

    // Update last login
    await db.query(
      "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = $1",
      [user.id]
    );

    // Set session
    req.session.userId = user.id;

    res.json({
      success: true,
      user: {
        id: user.id,
        email: user.email,
        username: user.username,
        role: user.role
      }
    });
  } catch (error) {
    console.error("Login error:", error);
    res.status(500).json({ error: "Login failed" });
  }
});

// Register with invite code
authRouter.post("/register", async (req, res) => {
  const { email, username, password, inviteCode } = req.body;

  if (!email || !username || !password || !inviteCode) {
    return res.status(400).json({ error: "All fields required" });
  }

  try {
    // Verify invite code
    const inviteResult = await db.query(
      `SELECT id, invited_by, expires_at, used 
       FROM invitations 
       WHERE invite_code = $1`,
      [inviteCode]
    );

    if (inviteResult.rows.length === 0) {
      return res.status(400).json({ error: "Invalid invite code" });
    }

    const invite = inviteResult.rows[0];

    if (invite.used) {
      return res.status(400).json({ error: "Invite code already used" });
    }

    if (new Date(invite.expires_at) < new Date()) {
      return res.status(400).json({ error: "Invite code expired" });
    }

    // Hash password
    const passwordHash = await bcrypt.hash(password, CONFIG.BCRYPT_SALT_ROUNDS);

    // Create user
    const userResult = await db.query(
      `INSERT INTO users (email, username, password_hash, invited_by)
       VALUES ($1, $2, $3, $4)
       RETURNING id, email, username, role`,
      [email, username, passwordHash, invite.invited_by]
    );

    const newUser = userResult.rows[0];

    // Mark invite as used
    await db.query(
      "UPDATE invitations SET used = true, used_by = $1 WHERE id = $2",
      [newUser.id, invite.id]
    );

    // Set session
    req.session.userId = newUser.id;

    res.json({
      success: true,
      user: {
        id: newUser.id,
        email: newUser.email,
        username: newUser.username,
        role: newUser.role
      }
    });
  } catch (error: any) {
    console.error("Registration error:", error);
    
    if (error.code === "23505") { // Unique constraint violation
      return res.status(400).json({ error: "Email or username already exists" });
    }
    
    res.status(500).json({ error: "Registration failed" });
  }
});

// Logout endpoint
authRouter.post("/logout", (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).json({ error: "Logout failed" });
    }
    res.json({ success: true });
  });
});

// Get current user
authRouter.get("/me", async (req, res) => {
  if (!req.session?.userId) {
    return res.status(401).json({ error: "Not authenticated" });
  }

  try {
    const result = await db.query(
      "SELECT id, email, username, role FROM users WHERE id = $1 AND is_active = true",
      [req.session.userId]
    );

    if (result.rows.length === 0) {
      return res.status(401).json({ error: "User not found" });
    }

    res.json({ user: result.rows[0] });
  } catch (error) {
    console.error("Get user error:", error);
    res.status(500).json({ error: "Failed to get user" });
  }
});
