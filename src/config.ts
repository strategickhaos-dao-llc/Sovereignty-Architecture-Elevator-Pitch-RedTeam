import fs from "fs";
import yaml from "js-yaml";

type C = {
  discord: { 
    bot: { 
      token_secret_env: string; 
      app_id?: string;
    }; 
    channels: { 
      prs: string; 
      deployments: string; 
      alerts: string;
      financial?: string;
      treasury?: string;
    } 
  };
  control_api: { base_url: string; bearer_env: string };
  event_gateway: { port: number };
  treasury?: {
    accounts_config: string;
    api_endpoint: string;
    swarmgate?: {
      allocation_percent: number;
      trigger_channel: string;
    };
  };
};

export function loadConfig(): C {
  const doc: C = yaml.load(fs.readFileSync("discovery.yml", "utf8")) as C;
  return doc;
}

export const env = (k: string, req = true) => {
  const v = process.env[k];
  if (!v && req) throw new Error(`Missing env ${k}`);
  return v || "";
};