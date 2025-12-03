import fs from "fs";
import yaml from "js-yaml";

type C = {
  discord: { 
    bot: { 
      token_secret_env: string;
      app_id?: string;
    };
    channels: { prs: string; deployments: string; alerts: string };
  };
  control_api: { base_url: string; bearer_env: string };
  event_gateway: { port: number };
  priority_council?: {
    enabled: boolean;
    discord: {
      channels: {
        priority_council: string;
        roadmap: string;
        auto_merges: string;
      };
    };
  };
};

export function loadConfig(): C {
  const doc: unknown = yaml.load(fs.readFileSync("discovery.yml", "utf8"));
  return doc as C;
}

export const env = (k: string, req = true) => {
  const v = process.env[k];
  if (!v && req) throw new Error(`Missing env ${k}`);
  return v || "";
};