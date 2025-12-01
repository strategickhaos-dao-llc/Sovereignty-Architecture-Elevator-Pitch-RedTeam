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
  refinory?: {
    enabled: boolean;
    ports: { api: number };
    experts: { team: { name: string }[]; orchestration: { strategy: string } };
    runtime: { gpu: boolean; workers: number };
  };
  ai_agents?: {
    model_name: string;
  };
};

export function loadConfig(): C {
  const doc: unknown = yaml.load(fs.readFileSync("discovery.yml", "utf8"));
  return doc as C;
}

export const env = (k: string, req = true): string => {
  const v = process.env[k];
  if (!v && req) throw new Error(`Missing env ${k}`);
  return v || "";
};