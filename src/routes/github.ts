import type { Request, Response } from "express";
import crypto from "crypto";
import { REST } from "discord.js";

const MAX_COMMENT_LENGTH = 200;

function sigOk(secret: string, raw: string, sig: string) {
  const h = crypto.createHmac("sha256", secret).update(raw).digest("hex");
  return `sha256=${h}` === sig;
}

export function githubRoutes(rest: REST, channelIds: Record<string,string>, secret: string) {
  return async (req: Request, res: Response) => {
    const sig = req.get("X-Hub-Signature-256") || "";
    const raw = (req as any).rawBody;
    if (!sigOk(secret, raw, sig)) return res.status(401).send("bad sig");
    const ev = req.get("X-GitHub-Event");
    const payload = req.body;

    const send = async (channelId: string, title: string, desc: string) => {
      await rest.post(`/channels/${channelId}/messages`, {
        body: { embeds: [{ title, description: desc, color: 3099199 }] }
      } as any);
    };

    if (ev === "pull_request") {
      const a = payload.action;
      const pr = payload.pull_request;
      await send(channelIds.prs, `PR ${a}: #${pr.number} ${pr.title}`, `${pr.user.login} → ${pr.base.repo.full_name}\n${pr.html_url}`);
    } else if (ev === "issue_comment") {
      const a = payload.action;
      const comment = payload.comment;
      const issue = payload.issue;
      const isPR = !!issue.pull_request;
      const type = isPR ? "PR" : "Issue";
      const commentBody = comment.body.length > MAX_COMMENT_LENGTH ? comment.body.substring(0, MAX_COMMENT_LENGTH) + "..." : comment.body;
      await send(channelIds.prs, `${type} Comment ${a}: #${issue.number} ${issue.title}`, `${comment.user.login}: ${commentBody}\n${comment.html_url}`);
    } else if (ev === "check_suite") {
      const cs = payload.check_suite;
      await send(channelIds.deployments, `Checks ${cs.status}`, `${cs.app.name} → ${cs.conclusion || "pending"}`);
    } else if (ev === "push") {
      await send(channelIds.deployments, `Push: ${payload.ref}`, `${payload.repository.full_name}\n${payload.compare}`);
    }
    res.send("ok");
  };
}