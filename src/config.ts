import fs from "fs";
import yaml from "js-yaml";

export interface ImmuneConfig {
  enabled: boolean;
  channels: {
    immune_response: string;
    swarm_health: string;
  };
  slash_commands: {
    inject_threat: { enabled: boolean };
    status: { enabled: boolean };
    antibody: { enabled: boolean };
    swarm_mode: { enabled: boolean };
  };
  cell_types: {
    rbc: { description: string; emoji: string };
    wbc: { description: string; emoji: string };
    platelet: { description: string; emoji: string };
  };
  behavioral_modes: string[];
}

export interface ClusterConfig {
  name: string;
  description: string;
  zone: string;
  api_server?: string;
  namespaces?: string[];
}

export interface DiscordConfig {
  guild_id: string | null;
  channels: {
    status: string;
    alerts: string;
    deployments: string;
    inference: string;
    agents: string;
    prs: string;
    dev_feed: string;
    immune_response?: string;
    swarm_health?: string;
  };
  bot: {
    app_id: string | null;
    token_secret_ref: string;
    intents: {
      message_content: boolean;
      guild_members: boolean;
    };
    rbac: {
      prod_role: string;
      allow_commands: string[];
      prod_protected_commands: string[];
    };
    rate_limits: {
      max_msgs_per_min: number;
      burst: number;
    };
  };
}

export interface InfraConfig {
  environments: string[];
  control_api: {
    base_url: string;
    bearer_env: string;
    auth?: {
      type: string;
      token_secret_ref: string;
    };
  };
  gke_clusters?: ClusterConfig[];
  message_bus: {
    type: string;
    url: string;
    topic_prefix: string;
  };
}

export interface Config {
  org: {
    name: string;
    contact: {
      owner: string;
      slack_or_discord_handle: string | null;
    };
  };
  discord: DiscordConfig;
  infra: InfraConfig;
  immune_system?: ImmuneConfig;
  event_gateway: {
    port: number;
    public_url: string;
  };
}

export function loadConfig(): Config {
  const configPath = process.env.DISCOVERY_CONFIG_PATH || "discovery.yml";
  const doc = yaml.load(fs.readFileSync(configPath, "utf8")) as Config;
  
  // Provide default control_api.bearer_env for backwards compatibility
  if (doc.infra?.control_api && !doc.infra.control_api.bearer_env) {
    doc.infra.control_api.bearer_env = "CTRL_API_TOKEN";
  }
  
  return doc;
}

export const env = (k: string, req = true): string => {
  const v = process.env[k];
  if (!v && req) throw new Error(`Missing env ${k}`);
  return v || "";
};