// RBAC guard for command handlers. Reads discovery.yml or an injected policy map.
// Example usage: const guard = new RbacGuard(discoveryMap); if (!guard.allowed(user, 'deploy')) throw 403

import fs from "fs";
import yaml from "js-yaml";

export type Discovery = {
  approvals?: {
    prod_commands_require?: string[];
  };
  command_map?: Record<string, string[]>; // command -> allowed roles
};

export class RbacGuard {
  discovery: Discovery;

  constructor(fromPathOrMap: string | Discovery) {
    if (typeof fromPathOrMap === "string") {
      const raw = fs.readFileSync(fromPathOrMap, "utf8");
      this.discovery = yaml.load(raw) as Discovery;
    } else {
      this.discovery = fromPathOrMap;
    }
  }

  // check if userRoles intersects required roles for a command
  allowed(userRoles: string[], command: string): boolean {
    const cmdRoles = this.discovery.command_map?.[command];
    if (cmdRoles && cmdRoles.length > 0) {
      return userRoles.some((r) => cmdRoles.includes(r));
    }

    // fallback to prod approvals map for prod-level commands
    if (this.discovery.approvals?.prod_commands_require?.length && this.isProdCommand(command)) {
      return userRoles.some((r) => this.discovery.approvals!.prod_commands_require!.includes(r));
    }

    // default allow (use cautiously)
    return true;
  }

  isProdCommand(command: string) {
    const prodCommands = ["deploy", "scale", "promote", "rollback"];
    return prodCommands.includes(command);
  }
}
