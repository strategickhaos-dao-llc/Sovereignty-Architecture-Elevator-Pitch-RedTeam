import fs from "fs";
import yaml from "js-yaml";

/**
 * RBAC Guard for Discord Bot Commands
 * Strategickhaos DAO LLC - Command Authorization
 * 
 * Features:
 * - Role-based command authorization
 * - Reads configuration from discovery.yml
 * - Supports protected commands requiring specific roles
 * - Audit logging for authorization decisions
 */

interface DiscordRbacConfig {
  prod_role: string;
  allow_commands: string[];
  prod_protected_commands: string[];
}

interface GovernanceConfig {
  approvals: {
    prod_commands_require: string[];
  };
}

interface DiscoveryConfig {
  discord?: {
    bot?: {
      rbac?: DiscordRbacConfig;
    };
  };
  governance?: GovernanceConfig;
}

interface AuthorizationResult {
  allowed: boolean;
  reason: string;
  requiredRoles?: string[];
}

// Cached configuration
let cachedConfig: DiscoveryConfig | null = null;
let configLoadTime = 0;
const CONFIG_CACHE_TTL_MS = 60000; // 1 minute cache

/**
 * Load discovery configuration with caching
 */
export function loadDiscoveryConfig(configPath: string = "discovery.yml"): DiscoveryConfig {
  const now = Date.now();
  
  if (cachedConfig && (now - configLoadTime) < CONFIG_CACHE_TTL_MS) {
    return cachedConfig;
  }

  try {
    const doc = yaml.load(fs.readFileSync(configPath, "utf8")) as DiscoveryConfig;
    cachedConfig = doc;
    configLoadTime = now;
    return doc;
  } catch (error) {
    console.error(`Failed to load discovery config: ${error}`);
    return {};
  }
}

/**
 * Clear the configuration cache (useful for testing)
 */
export function clearConfigCache(): void {
  cachedConfig = null;
  configLoadTime = 0;
}

/**
 * Get RBAC configuration from discovery.yml
 */
export function getRbacConfig(configPath?: string): DiscordRbacConfig {
  const config = loadDiscoveryConfig(configPath);
  return config.discord?.bot?.rbac || {
    prod_role: "ReleaseMgr",
    allow_commands: [],
    prod_protected_commands: []
  };
}

/**
 * Get governance approval requirements
 */
export function getGovernanceConfig(configPath?: string): GovernanceConfig {
  const config = loadDiscoveryConfig(configPath);
  return config.governance || {
    approvals: {
      prod_commands_require: ["ReleaseMgr"]
    }
  };
}

/**
 * Check if a command is protected (requires specific roles)
 */
export function isProtectedCommand(command: string, configPath?: string): boolean {
  const rbac = getRbacConfig(configPath);
  const normalizedCmd = command.startsWith("/") ? command : `/${command}`;
  return rbac.prod_protected_commands.some(
    cmd => normalizedCmd.toLowerCase() === cmd.toLowerCase()
  );
}

/**
 * Check if a command is allowed in the system
 */
export function isAllowedCommand(command: string, configPath?: string): boolean {
  const rbac = getRbacConfig(configPath);
  const normalizedCmd = command.startsWith("/") ? command : `/${command}`;
  return rbac.allow_commands.some(
    cmd => normalizedCmd.toLowerCase() === cmd.toLowerCase()
  );
}

/**
 * Get required roles for a command
 */
export function getRequiredRoles(command: string, configPath?: string): string[] {
  if (!isProtectedCommand(command, configPath)) {
    return []; // No roles required for non-protected commands
  }

  const governance = getGovernanceConfig(configPath);
  return governance.approvals.prod_commands_require;
}

/**
 * Check if user has required role
 */
export function hasRole(userRoles: string[], requiredRole: string): boolean {
  return userRoles.some(
    role => role.toLowerCase() === requiredRole.toLowerCase()
  );
}

/**
 * Check if user has any of the required roles
 */
export function hasAnyRole(userRoles: string[], requiredRoles: string[]): boolean {
  return requiredRoles.some(required => hasRole(userRoles, required));
}

/**
 * Authorize a command execution
 */
export function authorizeCommand(
  command: string,
  userRoles: string[],
  options: {
    environment?: string;
    userId?: string;
    configPath?: string;
  } = {}
): AuthorizationResult {
  const { environment = "dev", userId, configPath } = options;
  const normalizedCmd = command.startsWith("/") ? command : `/${command}`;

  // Check if command is allowed
  if (!isAllowedCommand(normalizedCmd, configPath)) {
    logAudit({
      action: "authorize",
      command: normalizedCmd,
      userId,
      allowed: false,
      reason: "Command not in allowed list"
    });
    return {
      allowed: false,
      reason: `Command ${normalizedCmd} is not allowed`
    };
  }

  // Check if command is protected
  if (!isProtectedCommand(normalizedCmd, configPath)) {
    logAudit({
      action: "authorize",
      command: normalizedCmd,
      userId,
      allowed: true,
      reason: "Non-protected command"
    });
    return {
      allowed: true,
      reason: "Command does not require special authorization"
    };
  }

  // For protected commands, check role requirements
  const requiredRoles = getRequiredRoles(normalizedCmd, configPath);
  
  // Production environment has stricter requirements
  if (environment === "prod") {
    if (!hasAnyRole(userRoles, requiredRoles)) {
      logAudit({
        action: "authorize",
        command: normalizedCmd,
        userId,
        environment,
        allowed: false,
        reason: "Missing required role for prod",
        requiredRoles
      });
      return {
        allowed: false,
        reason: `Protected command ${normalizedCmd} requires one of these roles: ${requiredRoles.join(", ")}`,
        requiredRoles
      };
    }
  }

  // For non-prod environments, also check roles for protected commands
  if (!hasAnyRole(userRoles, requiredRoles)) {
    logAudit({
      action: "authorize",
      command: normalizedCmd,
      userId,
      environment,
      allowed: false,
      reason: "Missing required role",
      requiredRoles
    });
    return {
      allowed: false,
      reason: `Protected command ${normalizedCmd} requires one of these roles: ${requiredRoles.join(", ")}`,
      requiredRoles
    };
  }

  logAudit({
    action: "authorize",
    command: normalizedCmd,
    userId,
    environment,
    allowed: true,
    reason: "Role requirements met"
  });

  return {
    allowed: true,
    reason: "Authorization successful"
  };
}

/**
 * Audit log entry
 */
interface AuditEntry {
  action: string;
  command: string;
  userId?: string;
  environment?: string;
  allowed: boolean;
  reason: string;
  requiredRoles?: string[];
}

/**
 * Log audit entry (can be extended to write to external sink)
 */
function logAudit(entry: AuditEntry): void {
  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    ...entry
  };
  
  // Log to stdout (can be picked up by Loki/Promtail)
  console.log(JSON.stringify({ level: "audit", ...logEntry }));
}

/**
 * Express middleware for RBAC authorization
 */
export function createRbacMiddleware(options: {
  getUserRoles: (req: any) => string[] | Promise<string[]>;
  getCommand: (req: any) => string;
  getEnvironment?: (req: any) => string;
  getUserId?: (req: any) => string | undefined;
  configPath?: string;
}) {
  return async (req: any, res: any, next: any) => {
    try {
      const userRoles = await Promise.resolve(options.getUserRoles(req));
      const command = options.getCommand(req);
      const environment = options.getEnvironment?.(req) || "dev";
      const userId = options.getUserId?.(req);

      const result = authorizeCommand(command, userRoles, {
        environment,
        userId,
        configPath: options.configPath
      });

      if (!result.allowed) {
        return res.status(403).json({
          error: "Forbidden",
          message: result.reason,
          requiredRoles: result.requiredRoles
        });
      }

      // Attach authorization result to request
      req.rbacResult = result;
      next();
    } catch (error) {
      console.error("RBAC middleware error:", error);
      return res.status(500).json({ error: "Authorization check failed" });
    }
  };
}

/**
 * Discord.js interaction RBAC check
 */
export async function checkInteractionRbac(
  interaction: { 
    commandName: string; 
    member?: { roles: { cache: Map<string, { name: string }> } | string[] } | null;
    user?: { id: string };
  },
  environment: string = "dev",
  configPath?: string
): Promise<AuthorizationResult> {
  // Extract user roles from Discord interaction
  const userRoles: string[] = [];
  if (interaction.member?.roles) {
    const roles = interaction.member.roles;
    if (Array.isArray(roles)) {
      // API member roles are string array of role IDs
      userRoles.push(...roles);
    } else if ('cache' in roles && roles.cache instanceof Map) {
      // GuildMember roles have cache Map
      for (const [, role] of roles.cache) {
        userRoles.push(role.name);
      }
    }
  }

  return authorizeCommand(interaction.commandName, userRoles, {
    environment,
    userId: interaction.user?.id,
    configPath
  });
}
