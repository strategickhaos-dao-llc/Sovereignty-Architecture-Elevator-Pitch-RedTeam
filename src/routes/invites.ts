import express from "express";
import { randomBytes } from "crypto";
import { db } from "../db.js";
import { AuthRequest, requireRole } from "../middleware/auth.js";

export const inviteRouter = express.Router();

// Generate invite code
inviteRouter.post("/generate", requireRole("admin"), async (req: AuthRequest, res) => {
  const { email, expiresInDays = 7 } = req.body;

  if (!email) {
    return res.status(400).json({ error: "Email required" });
  }

  try {
    // Generate unique invite code
    const inviteCode = randomBytes(32).toString("hex");
    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + expiresInDays);

    await db.query(
      `INSERT INTO invitations (invite_code, email, invited_by, expires_at)
       VALUES ($1, $2, $3, $4)`,
      [inviteCode, email, req.user!.id, expiresAt]
    );

    res.json({
      success: true,
      inviteCode,
      email,
      expiresAt,
      inviteUrl: `${process.env.BASE_URL || "http://localhost:8090"}/register?invite=${inviteCode}`
    });
  } catch (error) {
    console.error("Generate invite error:", error);
    res.status(500).json({ error: "Failed to generate invite" });
  }
});

// List invitations (admin only)
inviteRouter.get("/list", requireRole("admin"), async (req: AuthRequest, res) => {
  try {
    const result = await db.query(
      `SELECT i.id, i.invite_code, i.email, i.used, i.expires_at, i.created_at,
              u1.username as invited_by_username,
              u2.username as used_by_username
       FROM invitations i
       LEFT JOIN users u1 ON i.invited_by = u1.id
       LEFT JOIN users u2 ON i.used_by = u2.id
       ORDER BY i.created_at DESC
       LIMIT 100`
    );

    res.json({ invitations: result.rows });
  } catch (error) {
    console.error("List invites error:", error);
    res.status(500).json({ error: "Failed to list invitations" });
  }
});

// Get my invitations
inviteRouter.get("/mine", async (req: AuthRequest, res) => {
  try {
    const result = await db.query(
      `SELECT i.id, i.invite_code, i.email, i.used, i.expires_at, i.created_at,
              u.username as used_by_username
       FROM invitations i
       LEFT JOIN users u ON i.used_by = u.id
       WHERE i.invited_by = $1
       ORDER BY i.created_at DESC`,
      [req.user!.id]
    );

    res.json({ invitations: result.rows });
  } catch (error) {
    console.error("Get my invites error:", error);
    res.status(500).json({ error: "Failed to get invitations" });
  }
});

// Revoke invitation (admin only)
inviteRouter.delete("/:inviteId", requireRole("admin"), async (req: AuthRequest, res) => {
  const { inviteId } = req.params;

  try {
    await db.query(
      "DELETE FROM invitations WHERE id = $1",
      [inviteId]
    );

    res.json({ success: true });
  } catch (error) {
    console.error("Revoke invite error:", error);
    res.status(500).json({ error: "Failed to revoke invitation" });
  }
});

// Validate invite code (public endpoint)
inviteRouter.get("/validate/:code", async (req, res) => {
  const { code } = req.params;

  try {
    const result = await db.query(
      `SELECT email, expires_at, used 
       FROM invitations 
       WHERE invite_code = $1`,
      [code]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ valid: false, error: "Invalid invite code" });
    }

    const invite = result.rows[0];

    if (invite.used) {
      return res.status(400).json({ valid: false, error: "Invite code already used" });
    }

    if (new Date(invite.expires_at) < new Date()) {
      return res.status(400).json({ valid: false, error: "Invite code expired" });
    }

    res.json({ valid: true, email: invite.email });
  } catch (error) {
    console.error("Validate invite error:", error);
    res.status(500).json({ error: "Failed to validate invite" });
  }
});
