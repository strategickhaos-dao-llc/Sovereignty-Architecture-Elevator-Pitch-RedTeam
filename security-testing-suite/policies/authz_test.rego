# authz_test.rego - Comprehensive Test Suite for Authorization Policy
# Strategickhaos Sovereign Infrastructure
#
# Test coverage:
# - Role-based access control (admin, moderator, user, guest)
# - Resource ownership validation
# - Action-based permissions
# - Edge cases (null, empty, malformed inputs)
# - Audit log structure validation

package authz_test

import future.keywords.if
import data.authz

# =============================================================================
# Admin Role Tests
# =============================================================================

test_admin_can_read if {
    authz.allow with input as {
        "user": {"id": "admin-1", "role": "admin"},
        "action": "read",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "other-user"}
    }
}

test_admin_can_write if {
    authz.allow with input as {
        "user": {"id": "admin-1", "role": "admin"},
        "action": "write",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "other-user"}
    }
}

test_admin_can_delete if {
    authz.allow with input as {
        "user": {"id": "admin-1", "role": "admin"},
        "action": "delete",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "other-user"}
    }
}

test_admin_can_access_protected_resources if {
    authz.allow with input as {
        "user": {"id": "admin-1", "role": "admin"},
        "action": "read",
        "path": "/api/v1/admin/users",
        "resource": {}
    }
}

test_admin_can_access_admin_endpoint if {
    authz.allow with input as {
        "user": {"id": "admin-1", "role": "admin"},
        "action": "admin",
        "path": "/api/v1/admin/settings",
        "resource": {}
    }
}

# =============================================================================
# Moderator Role Tests
# =============================================================================

test_moderator_can_read if {
    authz.allow with input as {
        "user": {"id": "mod-1", "role": "moderator"},
        "action": "read",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "other-user"}
    }
}

test_moderator_can_write if {
    authz.allow with input as {
        "user": {"id": "mod-1", "role": "moderator"},
        "action": "write",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "other-user"}
    }
}

test_moderator_cannot_delete if {
    not authz.allow with input as {
        "user": {"id": "mod-1", "role": "moderator"},
        "action": "delete",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "other-user"}
    }
}

test_moderator_can_moderate if {
    authz.allow with input as {
        "user": {"id": "mod-1", "role": "moderator"},
        "action": "moderate",
        "path": "/api/v1/content/456",
        "resource": {"id": "456", "owner_id": "user-1"}
    }
}

test_moderator_cannot_access_admin_resources if {
    not authz.allow with input as {
        "user": {"id": "mod-1", "role": "moderator"},
        "action": "read",
        "path": "/api/v1/admin/users",
        "resource": {}
    }
}

# =============================================================================
# User Role Tests
# =============================================================================

test_user_can_read_own_resource if {
    authz.allow with input as {
        "user": {"id": "user-1", "role": "user"},
        "action": "read",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "user-1"}
    }
}

test_user_can_write_own_resource if {
    authz.allow with input as {
        "user": {"id": "user-1", "role": "user"},
        "action": "write",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "user-1"}
    }
}

test_user_cannot_delete if {
    not authz.allow with input as {
        "user": {"id": "user-1", "role": "user"},
        "action": "delete",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "user-1"}
    }
}

test_user_cannot_access_others_resource if {
    not authz.allow with input as {
        "user": {"id": "user-1", "role": "user"},
        "action": "read",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "other-user"}
    }
}

test_user_cannot_access_admin_resources if {
    not authz.allow with input as {
        "user": {"id": "user-1", "role": "user"},
        "action": "read",
        "path": "/api/v1/admin/settings",
        "resource": {}
    }
}

test_user_can_access_team_resource if {
    authz.allow with input as {
        "user": {"id": "user-1", "role": "user", "teams": ["team-alpha"]},
        "action": "read",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "other-user", "team_id": "team-alpha"}
    }
}

test_user_cannot_moderate if {
    not authz.allow with input as {
        "user": {"id": "user-1", "role": "user"},
        "action": "moderate",
        "path": "/api/v1/content/456",
        "resource": {"id": "456", "owner_id": "user-1"}
    }
}

# =============================================================================
# Guest Role Tests
# =============================================================================

test_guest_can_access_public_resource if {
    authz.allow with input as {
        "user": {"id": "guest-1", "role": "guest"},
        "action": "read",
        "path": "/health",
        "resource": {}
    }
}

test_guest_cannot_write if {
    not authz.allow with input as {
        "user": {"id": "guest-1", "role": "guest"},
        "action": "write",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "guest-1"}
    }
}

test_guest_cannot_access_protected_resource if {
    not authz.allow with input as {
        "user": {"id": "guest-1", "role": "guest"},
        "action": "read",
        "path": "/api/v1/admin/users",
        "resource": {}
    }
}

# =============================================================================
# Public Resource Tests
# =============================================================================

test_public_health_endpoint if {
    authz.allow with input as {
        "user": {},
        "action": "read",
        "path": "/health",
        "resource": {}
    }
}

test_public_metrics_endpoint if {
    authz.allow with input as {
        "user": {},
        "action": "read",
        "path": "/metrics",
        "resource": {}
    }
}

test_public_docs_endpoint if {
    authz.allow with input as {
        "user": {},
        "action": "read",
        "path": "/docs",
        "resource": {}
    }
}

test_public_api_endpoint if {
    authz.allow with input as {
        "user": {},
        "action": "read",
        "path": "/api/v1/public/info",
        "resource": {}
    }
}

# =============================================================================
# Edge Cases - Null and Empty Values
# =============================================================================

test_null_user_denied if {
    not authz.allow with input as {
        "user": null,
        "action": "read",
        "path": "/api/v1/resources/123",
        "resource": {}
    }
}

test_empty_user_id_denied if {
    not authz.allow with input as {
        "user": {"id": "", "role": "user"},
        "action": "read",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": ""}
    }
}

test_null_user_id_denied if {
    not authz.allow with input as {
        "user": {"id": null, "role": "user"},
        "action": "read",
        "path": "/api/v1/resources/123",
        "resource": {}
    }
}

test_invalid_role_denied if {
    not authz.allow with input as {
        "user": {"id": "user-1", "role": "superadmin"},
        "action": "read",
        "path": "/api/v1/resources/123",
        "resource": {}
    }
}

test_missing_action_denied if {
    not authz.allow with input as {
        "user": {"id": "user-1", "role": "user"},
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "user-1"}
    }
}

test_invalid_action_denied if {
    not authz.allow with input as {
        "user": {"id": "user-1", "role": "user"},
        "action": "superdelete",
        "path": "/api/v1/resources/123",
        "resource": {}
    }
}

# =============================================================================
# Audit Log Structure Tests
# =============================================================================

test_audit_entry_has_timestamp if {
    entry := authz.audit_entry with input as {
        "user": {"id": "user-1", "role": "user"},
        "action": "read",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "user-1"}
    }
    entry.timestamp > 0
}

test_audit_entry_has_user_id if {
    entry := authz.audit_entry with input as {
        "user": {"id": "user-1", "role": "user"},
        "action": "read",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "user-1"}
    }
    entry.user_id == "user-1"
}

test_audit_entry_has_action if {
    entry := authz.audit_entry with input as {
        "user": {"id": "user-1", "role": "user"},
        "action": "read",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "user-1"}
    }
    entry.action == "read"
}

test_audit_entry_has_resource_path if {
    entry := authz.audit_entry with input as {
        "user": {"id": "user-1", "role": "user"},
        "action": "read",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "user-1"}
    }
    entry.resource_path == "/api/v1/resources/123"
}

test_audit_entry_has_decision if {
    entry := authz.audit_entry with input as {
        "user": {"id": "user-1", "role": "user"},
        "action": "read",
        "path": "/api/v1/resources/123",
        "resource": {"id": "123", "owner_id": "user-1"}
    }
    entry.allowed == true
}

# =============================================================================
# Rate Limiting Tier Tests
# =============================================================================

test_admin_rate_limit_tier if {
    tier := authz.rate_limit_tier with input as {
        "user": {"id": "admin-1", "role": "admin"}
    }
    tier == "unlimited"
}

test_moderator_rate_limit_tier if {
    tier := authz.rate_limit_tier with input as {
        "user": {"id": "mod-1", "role": "moderator"}
    }
    tier == "high"
}

test_user_rate_limit_tier if {
    tier := authz.rate_limit_tier with input as {
        "user": {"id": "user-1", "role": "user"}
    }
    tier == "standard"
}

test_guest_rate_limit_tier if {
    tier := authz.rate_limit_tier with input as {
        "user": {"id": "guest-1", "role": "guest"}
    }
    tier == "limited"
}

# =============================================================================
# Permission Helper Tests
# =============================================================================

test_admin_has_all_permissions if {
    perms := authz.user_permissions with input as {
        "user": {"role": "admin"}
    }
    perms.can_read == true
    perms.can_write == true
    perms.can_delete == true
    perms.can_admin == true
}

test_user_has_limited_permissions if {
    perms := authz.user_permissions with input as {
        "user": {"role": "user"}
    }
    perms.can_read == true
    perms.can_write == true
    perms.can_delete == false
    perms.can_admin == false
}
