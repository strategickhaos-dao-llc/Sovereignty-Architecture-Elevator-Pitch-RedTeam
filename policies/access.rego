# Access Control Policy for Strategickhaos DAO
# OPA Rego Policy for role-based access control
#
# This policy defines access rules based on user roles:
# - admin: Full access (allow)
# - owner: Full access (allow)
# - user: Restricted access (deny by default)
# - guest: Restricted access (deny by default)
# - Invalid/missing roles: Denied

package access

default allow := false

# Admin role gets full access
allow if {
    input.role == "admin"
}

# Owner role gets full access
allow if {
    input.role == "owner"
}
