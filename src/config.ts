import fs from "fs";
import yaml from "js-yaml";

interface DiscordConfig {
  guild_id: string | null;
  channels: {
    status: string;
    alerts: string;
    deployments: string;
    inference: string;
    agents: string;
    prs: string;
    dev_feed: string;
    financial?: string;
    treasury?: string;
  };
  bot: {
    app_id: string | null;
    token_secret_ref: string;
  };
}

interface InfraConfig {
  environments: string[];
  control_api: {
    base_url: string;
    auth: {
      type: string;
      token_secret_ref: string;
    };
  };
}

interface TreasuryConfig {
  enabled: boolean;
  accounts_config: string;
  api_endpoint: string;
  swarmgate: {
    allocation_percent: number;
    trigger_channel: string;
  };
}

export interface Config {
  discord: DiscordConfig;
  infra: InfraConfig;
  treasury?: TreasuryConfig;
  event_gateway?: {
    port: number;
  };
}

export function loadConfig(): Config {
  const doc = yaml.load(fs.readFileSync("discovery.yml", "utf8")) as Config;
  return doc;
}

export const env = (k: string, req = true) => {
  const v = process.env[k];
  if (!v && req) throw new Error(`Missing env ${k}`);
  return v || "";
};