import fs from "fs";
import yaml from "js-yaml";

type DiscordBot = {
  app_id: string | null;
  token_secret_ref: string;
  intents: { message_content: boolean; guild_members: boolean };
  rbac: {
    prod_role: string;
    allow_commands: string[];
    prod_protected_commands: string[];
  };
  rate_limits: { max_msgs_per_min: number; burst: number };
};

type DiscordChannels = {
  status: string;
  alerts: string;
  deployments: string;
  inference: string;
  agents: string;
  prs: string;
  dev_feed: string;
};

type ControlApi = {
  base_url: string;
  auth: { type: string; token_secret_ref: string };
  network: { access: string; cidrs_allowed: string[] };
};

type EventGateway = {
  public_url: string;
  auth: { hmac: { key_secret_ref: string; header: string; algo: string } };
  endpoints: Array<{
    path: string;
    allowed_services?: string[];
    discord_channel?: string;
    verify?: string;
    routes?: Array<{
      event: string;
      actions?: string[];
      branches?: string[];
      discord_channel: string;
    }>;
  }>;
};

type C = {
  org: { name: string; contact: { owner: string; slack_or_discord_handle: string | null }; compliance: string[] };
  discord: { guild_id: string | null; channels: DiscordChannels; bot: DiscordBot };
  infra: { environments: string[]; control_api: ControlApi; message_bus: { type: string; url: string; topic_prefix: string } };
  ai_agents: { enabled: boolean; model_provider: string; model_name: string; routing: { per_channel: Record<string, string> } };
  git: { provider: string; org: string; repos: Array<{ name: string; channel: string; env: string }> };
  event_gateway: EventGateway;
  commands: { enabled: boolean; list: Array<{ name: string; description: string; protected?: boolean; params: Array<{ name: string; type: string; required?: boolean; default?: number; enum?: string[] }> }> };
};

export function loadConfig(): C {
  const doc = yaml.load(fs.readFileSync("discovery.yml", "utf8")) as C;
  return doc;
}

export const env = (k: string, req = true) => {
  const v = process.env[k];
  if (!v && req) throw new Error(`Missing env ${k}`);
  return v || "";
};