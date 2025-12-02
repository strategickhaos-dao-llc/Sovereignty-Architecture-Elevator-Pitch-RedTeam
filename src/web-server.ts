import express from "express";
import session from "express-session";
import path from "path";
import { fileURLToPath } from "url";
import { authRouter } from "./routes/auth.js";
import { inviteRouter } from "./routes/invites.js";
import { llmRouter } from "./routes/llm.js";
import { requireAuth } from "./middleware/auth.js";
import { auditLogger } from "./middleware/audit.js";
import { rateLimiter } from "./middleware/ratelimit.js";
import { csrfProtection } from "./middleware/csrf.js";
import { CONFIG } from "./config/constants.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

// Security middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Session configuration with CSRF protection via SameSite
app.use(session({
  secret: process.env.SESSION_SECRET || "sovereignty-secret-change-in-production",
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === "production", // HTTPS only in production
    httpOnly: true, // Prevent XSS attacks
    sameSite: "strict", // CSRF protection - cookies only sent for same-site requests
    maxAge: CONFIG.SESSION_MAX_AGE_MS
  }
}));

// Audit logging middleware
app.use(auditLogger);

// Serve static files (HTML, CSS, JS)
app.use(express.static(path.join(__dirname, "../public")));

// Health check endpoint (no rate limiting)
app.get("/health", (_req, res) => {
  res.json({ status: "ok", service: "sovereignty-web" });
});

// API routes with rate limiting and CSRF protection
app.use("/api/auth", rateLimiter, csrfProtection, authRouter);
app.use("/api/invites", rateLimiter, csrfProtection, requireAuth, inviteRouter);
app.use("/api/llm", rateLimiter, csrfProtection, requireAuth, llmRouter);

// Serve index.html for all other routes (SPA)
app.get("*", (_req, res) => {
  res.sendFile(path.join(__dirname, "../public/index.html"));
});

const PORT = process.env.WEB_PORT || 8090;

app.listen(PORT, () => {
  console.log(`Invite-only web server running on port ${PORT}`);
});

export default app;
