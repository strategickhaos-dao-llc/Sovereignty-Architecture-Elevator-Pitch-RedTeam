// Jest-style unit tests for verifyHmac
import express from "express";
import request from "supertest";
import { verifyHmac } from "../verify_hmac.js";
import crypto from "crypto";

describe("verifyHmac middleware", () => {
  const secret = "shhh";
  const app = express();
  
  // raw body preservation
  app.use((req, res, next) => {
    const chunks: Buffer[] = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => {
      (req as any).rawBody = Buffer.concat(chunks);
      next();
    });
  });
  
  app.post(
    "/hook",
    verifyHmac({
      secretResolver: async () => secret,
      replayTtlSeconds: 2,
    }),
    (req, res) => res.status(200).send("ok")
  );

  test("accepts valid signature and nonce", async () => {
    const body = JSON.stringify({ hi: "there" });
    const sig = `sha256=${crypto.createHmac("sha256", secret).update(Buffer.from(body)).digest("hex")}`;
    const res = await request(app).post("/hook").set("x-hub-signature-256", sig).set("x-event-nonce", "n1").send(body);
    expect(res.status).toBe(200);
  });

  test("rejects missing signature header", async () => {
    const body = JSON.stringify({ hi: "there" });
    const res = await request(app).post("/hook").set("x-event-nonce", "n-missing-sig").send(body);
    expect(res.status).toBe(400);
    expect(res.text).toBe("Missing signature header");
  });

  test("rejects invalid signature", async () => {
    const body = JSON.stringify({ hi: "there" });
    const sig = `sha256=invalid_signature_here`;
    const res = await request(app).post("/hook").set("x-hub-signature-256", sig).set("x-event-nonce", "n-invalid").send(body);
    expect(res.status).toBe(401);
  });

  test("rejects missing nonce", async () => {
    const body = JSON.stringify({ hi: "no-nonce" });
    const sig = `sha256=${crypto.createHmac("sha256", secret).update(Buffer.from(body)).digest("hex")}`;
    const res = await request(app).post("/hook").set("x-hub-signature-256", sig).send(body);
    expect(res.status).toBe(400);
    expect(res.text).toBe("Missing nonce for replay protection");
  });

  test("rejects replay", async () => {
    const body = JSON.stringify({ hi: "again" });
    const sig = `sha256=${crypto.createHmac("sha256", secret).update(Buffer.from(body)).digest("hex")}`;
    await request(app).post("/hook").set("x-hub-signature-256", sig).set("x-event-nonce", "n2").send(body);
    const res2 = await request(app).post("/hook").set("x-hub-signature-256", sig).set("x-event-nonce", "n2").send(body);
    expect(res2.status).toBe(409);
    expect(res2.text).toBe("Replay detected");
  });
});
