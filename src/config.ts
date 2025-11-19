import fs from "fs";
import yaml from "js-yaml";

export type Config = {
  org: { name: string; contact: { owner: string; slack_or_discord_handle: string | null } };
  discord: { 
    guild_id: string | null;
    bot: { 
      app_id: string | null; 
      token_secret_ref: string;
    }; 
    channels: { 
      status: string;
      alerts: string; 
      deployments: string; 
      prs: string;
      inference: string;
      agents: string;
      dev_feed: string;
    } 
  };
  control_api: { base_url: string; auth: { type: string; token_secret_ref: string } };
  event_gateway: { public_url: string };
  infra: any;
  ai_agents: any;
  git: any;
  refinory: any;
  security: any;
  governance: any;
};

export function loadConfig(): Config {
  const doc: any = yaml.load(fs.readFileSync("discovery.yml", "utf8"));
  return doc;
}

export const config = loadConfig();

export const env = (k: string, req = true) => {
  const v = process.env[k];
  if (!v && req) throw new Error(`Missing env ${k}`);
  return v || "";
};