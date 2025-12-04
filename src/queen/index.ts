#!/usr/bin/env node

// Queen.js Entry Point
// Central webhook receiver for the Sovereignty Architecture
// Run with: npm run queen

import { startQueenServer, shutdownQueen } from "./server.js";

const config = {
  port: Number(process.env.QUEEN_PORT || process.env.PORT || 8081),
  natsUrl: process.env.NATS_URL || "nats://localhost:4222",
  githubWebhookSecret: process.env.GITHUB_WEBHOOK_SECRET
};

console.log("👑 Queen.js Webhook Receiver - Sovereignty Architecture");
console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
console.log(`📍 Port: ${config.port}`);
console.log(`📡 NATS: ${config.natsUrl}`);
console.log(`🔐 GitHub Secret: ${config.githubWebhookSecret ? "configured" : "not set"}`);
console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");

// Handle graceful shutdown
process.on("SIGINT", async () => {
  console.log("\n👑 Queen shutting down gracefully...");
  await shutdownQueen();
  process.exit(0);
});

process.on("SIGTERM", async () => {
  console.log("\n👑 Queen received SIGTERM...");
  await shutdownQueen();
  process.exit(0);
});

// Start the server
startQueenServer(config).catch((err) => {
  console.error("❌ Failed to start Queen:", err);
  process.exit(1);
});
