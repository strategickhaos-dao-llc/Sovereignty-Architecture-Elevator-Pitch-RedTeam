"""
RBAC (Role-Based Access Control) Module

Handles permission checks for Discord commands based on user roles.

LLM Directive: When adding new protected commands:
1. Add the permission name to PERMISSION_ROLES mapping
2. Apply @check_permission("permission_name") decorator to command
3. Document the required role in command docstring
"""

import functools
import logging
from typing import Callable, Optional, Set

import discord

logger = logging.getLogger(__name__)

# Permission to Discord role mapping
# These map permission names to required Discord role names
PERMISSION_ROLES: dict[str, Set[str]] = {
    "deploy": {"ReleaseMgr", "Admin", "DevOps"},
    "scale": {"ReleaseMgr", "Admin", "DevOps"},
    "logs": {"Developer", "ReleaseMgr", "Admin", "DevOps"},
    "status": {"Developer", "ReleaseMgr", "Admin", "DevOps", "Viewer"},
    "ask": {"Developer", "ReleaseMgr", "Admin", "DevOps", "Viewer"},
}

# Production-protected commands (require additional approval)
PROD_PROTECTED_COMMANDS: Set[str] = {"deploy", "scale"}


class RBACManager:
    """
    Manages role-based access control for bot commands.
    
    LLM Directive: Extend this class to:
    - Add database-backed role storage
    - Implement dynamic role assignment
    - Add approval workflows for production commands
    """
    
    def __init__(self):
        self.permission_roles = PERMISSION_ROLES.copy()
        self.prod_protected = PROD_PROTECTED_COMMANDS.copy()
    
    def has_permission(self, member: discord.Member, permission: str) -> bool:
        """
        Check if a member has the required permission.
        
        Args:
            member: Discord member to check
            permission: Permission name to verify
            
        Returns:
            True if member has required role, False otherwise
        """
        if permission not in self.permission_roles:
            logger.warning("Unknown permission requested: %s", permission)
            return False
        
        required_roles = self.permission_roles[permission]
        member_roles = {role.name for role in member.roles}
        
        # Check if member has any of the required roles
        has_access = bool(member_roles & required_roles)
        
        if not has_access:
            logger.info(
                "Permission denied: user=%s permission=%s roles=%s",
                member.name, permission, member_roles
            )
        
        return has_access
    
    def is_prod_protected(self, permission: str) -> bool:
        """Check if permission is protected for production."""
        return permission in self.prod_protected
    
    def add_role_mapping(self, permission: str, roles: Set[str]):
        """Add or update a permission to role mapping."""
        self.permission_roles[permission] = roles
    
    def get_required_roles(self, permission: str) -> Set[str]:
        """Get the roles required for a permission."""
        return self.permission_roles.get(permission, set())


# Global RBAC manager instance
_rbac_manager: Optional[RBACManager] = None


def get_rbac_manager() -> RBACManager:
    """Get or create the global RBAC manager."""
    global _rbac_manager
    if _rbac_manager is None:
        _rbac_manager = RBACManager()
    return _rbac_manager


def check_permission(permission: str):
    """
    Decorator to check if user has required permission.
    
    Usage:
        @check_permission("deploy")
        async def deploy(interaction: discord.Interaction, ...):
            ...
    
    LLM Directive: This decorator should be applied to all commands
    that modify system state or access sensitive information.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(interaction: discord.Interaction, *args, **kwargs):
            rbac = get_rbac_manager()
            
            # Check if user has permission
            if not rbac.has_permission(interaction.user, permission):
                required = rbac.get_required_roles(permission)
                await interaction.response.send_message(
                    f"❌ Permission denied. Required roles: {', '.join(required)}",
                    ephemeral=True
                )
                return
            
            # Check for production protection
            if rbac.is_prod_protected(permission):
                # Log the elevated access
                logger.info(
                    "Production command executed: user=%s command=%s",
                    interaction.user.name, func.__name__
                )
            
            return await func(interaction, *args, **kwargs)
        
        return wrapper
    return decorator


async def require_approval(interaction: discord.Interaction, command: str) -> bool:
    """
    Request approval for a protected command.
    
    LLM Directive: Implement this to:
    - Create an approval request in a designated channel
    - Wait for approval from authorized users
    - Timeout after configured duration
    - Return True if approved, False otherwise
    """
    # TODO: Implement approval workflow
    # This would create a thread/message requesting approval
    # and wait for reaction or button click from approvers
    
    logger.info("Approval requested for %s by %s", command, interaction.user.name)
    return True  # Stub: always approve for now
