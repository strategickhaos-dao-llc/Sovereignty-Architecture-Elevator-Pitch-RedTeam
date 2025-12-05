# authz.rego - Production-Ready Authorization Policy
# Strategickhaos Sovereign Infrastructure - RBAC Authorization
# 
# This policy implements role-based access control (RBAC) with:
# - Role hierarchy (admin > moderator > user)
# - Resource ownership validation
# - Action-based permissions
# - Audit logging for compliance

package authz

import future.keywords.if
import future.keywords.in
import future.keywords.contains

# Default deny - secure by default
default allow := false

# Role definitions with hierarchical permissions
roles := {
    "admin": {
        "can_read": true,
        "can_write": true,
        "can_delete": true,
        "can_admin": true,
        "can_moderate": true
    },
    "moderator": {
        "can_read": true,
        "can_write": true,
        "can_delete": false,
        "can_admin": false,
        "can_moderate": true
    },
    "user": {
        "can_read": true,
        "can_write": true,
        "can_delete": false,
        "can_admin": false,
        "can_moderate": false
    },
    "guest": {
        "can_read": true,
        "can_write": false,
        "can_delete": false,
        "can_admin": false,
        "can_moderate": false
    }
}

# Action to permission mapping
action_permissions := {
    "read": "can_read",
    "list": "can_read",
    "view": "can_read",
    "create": "can_write",
    "update": "can_write",
    "write": "can_write",
    "delete": "can_delete",
    "admin": "can_admin",
    "moderate": "can_moderate",
    "approve": "can_moderate",
    "reject": "can_moderate"
}

# Protected resources requiring special permissions
protected_resources := {
    "/api/v1/admin",
    "/api/v1/admin/users",
    "/api/v1/admin/settings",
    "/api/v1/admin/audit",
    "/api/v1/system/config"
}

# Public resources accessible without authentication
public_resources := {
    "/health",
    "/metrics",
    "/api/v1/public",
    "/docs",
    "/redoc",
    "/openapi.json"
}

# Allow access to public resources without authentication
allow if {
    is_public_resource
}

# Main authorization rule
allow if {
    not is_public_resource
    valid_user
    has_permission
    resource_access_allowed
}

# Check if resource is public
is_public_resource if {
    some resource in public_resources
    startswith(input.path, resource)
}

# Validate user has required fields
valid_user if {
    input.user.id != null
    input.user.id != ""
    input.user.role != null
    input.user.role in object.keys(roles)
}

# Check if user role has required permission for action
has_permission if {
    user_role := input.user.role
    action := input.action
    
    # Get permission key for action
    permission_key := action_permissions[action]
    
    # Check if role has permission
    roles[user_role][permission_key] == true
}

# Check resource-level access (ownership or admin)
resource_access_allowed if {
    # Admins can access all resources
    input.user.role == "admin"
}

resource_access_allowed if {
    # Moderators can access non-admin resources
    input.user.role == "moderator"
    not is_protected_resource
}

resource_access_allowed if {
    # Users can access their own resources
    input.user.role == "user"
    not is_protected_resource
    is_resource_owner
}

resource_access_allowed if {
    # Users can access shared/team resources
    input.user.role == "user"
    not is_protected_resource
    is_team_resource
}

resource_access_allowed if {
    # Guests can only access public resources (handled separately)
    input.user.role == "guest"
    is_public_resource
}

# Check if current resource is protected
is_protected_resource if {
    some resource in protected_resources
    startswith(input.path, resource)
}

# Check if user owns the resource
is_resource_owner if {
    input.resource.owner_id == input.user.id
}

# Check if resource belongs to user's team
is_team_resource if {
    input.resource.team_id != null
    input.resource.team_id in input.user.teams
}

# Audit log entry generation
audit_entry := entry if {
    entry := {
        "timestamp": time.now_ns(),
        "user_id": input.user.id,
        "user_role": input.user.role,
        "action": input.action,
        "resource_path": input.path,
        "resource_id": object.get(input.resource, "id", null),
        "allowed": allow,
        "reason": decision_reason
    }
}

# Decision reason for audit logging
decision_reason := "public_resource" if {
    is_public_resource
}

decision_reason := "role_permission_granted" if {
    not is_public_resource
    valid_user
    has_permission
    resource_access_allowed
}

decision_reason := "invalid_user" if {
    not valid_user
}

decision_reason := "insufficient_permission" if {
    valid_user
    not has_permission
}

decision_reason := "resource_access_denied" if {
    valid_user
    has_permission
    not resource_access_allowed
}

# Helper: Get user's effective permissions
user_permissions[permission] := value if {
    user_role := input.user.role
    role_perms := roles[user_role]
    some permission, value in role_perms
}

# Rate limiting hints (for integration with API gateway)
rate_limit_tier := tier if {
    input.user.role == "admin"
    tier := "unlimited"
}

rate_limit_tier := tier if {
    input.user.role == "moderator"
    tier := "high"
}

rate_limit_tier := tier if {
    input.user.role == "user"
    tier := "standard"
}

rate_limit_tier := tier if {
    input.user.role == "guest"
    tier := "limited"
}

rate_limit_tier := tier if {
    not input.user.role
    tier := "anonymous"
}
