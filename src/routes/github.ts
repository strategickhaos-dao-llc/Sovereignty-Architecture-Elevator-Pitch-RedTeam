import type { Request, Response } from "express";
import crypto from "crypto";
import { REST, RESTPostAPIChannelMessageJSONBody, Routes } from "discord.js";

interface RequestWithRawBody extends Request {
  rawBody?: string;
}

function sigOk(secret: string, raw: string, sig: string): boolean {
  if (!secret) return true; // Skip verification if no secret configured
  const h = crypto.createHmac("sha256", secret).update(raw).digest("hex");
  return `sha256=${h}` === sig;
}

export function githubRoutes(rest: REST, channelIds: Record<string, string>, secret: string) {
  return async (req: RequestWithRawBody, res: Response) => {
    const sig = req.get("X-Hub-Signature-256") || "";
    const raw = req.rawBody || "";
    if (!sigOk(secret, raw, sig)) return res.status(401).send("bad sig");
    const ev = req.get("X-GitHub-Event");
    const payload = req.body;

    const send = async (channelId: string, title: string, desc: string) => {
      if (!channelId) {
        console.warn(`No channel ID configured for notification: ${title}`);
        return;
      }
      const body: RESTPostAPIChannelMessageJSONBody = {
        embeds: [{ title, description: desc, color: 3099199 }]
      };
      await rest.post(Routes.channelMessages(channelId), { body });
    };

    try {
      if (ev === "pull_request") {
        const a = payload.action;
        const pr = payload.pull_request;
        await send(channelIds.prs, `PR ${a}: #${pr.number} ${pr.title}`, `${pr.user.login} → ${pr.base.repo.full_name}\n${pr.html_url}`);
      } else if (ev === "check_suite") {
        const cs = payload.check_suite;
        await send(channelIds.deployments, `Checks ${cs.status}`, `${cs.app.name} → ${cs.conclusion || "pending"}`);
      } else if (ev === "push") {
        await send(channelIds.deployments, `Push: ${payload.ref}`, `${payload.repository.full_name}\n${payload.compare}`);
      }
      res.send("ok");
    } catch (error) {
      console.error("Error processing GitHub webhook:", error);
      res.status(500).send("error");
    }
  };
}