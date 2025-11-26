import fs from "fs";
import yaml from "js-yaml";

type C = {
  discord: { 
    bot: { 
      token_secret_env: string;
      app_id?: string;
    }; 
    channels: { prs: string; deployments: string; alerts: string } 
  };
  control_api: { base_url: string; bearer_env: string };
  event_gateway: { port: number };
  ai_agents?: {
    enabled: boolean;
    model_provider: string;
    model_name: string;
    family_dom?: {
      enabled: boolean;
      layers: Record<string, boolean>;
      profiles: { persistence: string; max_memory_entries: number; session_timeout_hours: number };
      symbolic_throughput: Record<string, boolean | number>;
      signature_thresholds: Record<string, number>;
      channel_routing: Record<string, string>;
    };
  };
  refinory?: Record<string, unknown>;
};

export function loadConfig(): C {
  const doc: any = yaml.load(fs.readFileSync("discovery.yml", "utf8"));
  return doc;
}

export const env = (k: string, req = true) => {
  const v = process.env[k];
  if (!v && req) throw new Error(`Missing env ${k}`);
  return v || "";
};