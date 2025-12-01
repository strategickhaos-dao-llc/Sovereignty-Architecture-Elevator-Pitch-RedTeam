# Governance Directory

This directory contains governance policies, access control matrices, and authorization models for the Strategickhaos Sovereignty Architecture project.

---

## 📋 Files in This Directory

### `access_matrix.yaml`
**Purpose:** Defines role-based access control for human participants

**Key Sections:**
- **Roles:** drafter, approver, signer, auditor
- **Permissions:** What each role can do
- **Enforcement:** Repository and CI/CD checks

**Use Case:** Defines who can draft, review, approve, and sign legal documents and governance decisions

**Updated:** Previously created  
**Review Cycle:** Quarterly

---

### `agent_permissions.yaml`
**Purpose:** Explicit permission model for GitHub Copilot Agents and automation

**Key Sections:**
- **Agent Identity:** GitHub App scopes and authorization
- **Repository Access:** What files agents can/cannot edit
- **Infrastructure Boundaries:** What systems agents CANNOT access
- **Workflow Permissions:** PR creation, review, and merge rules
- **Audit & Monitoring:** Logging and alerting configuration

**Use Case:** Defines the security boundaries and blast-radius control for AI agents operating in the repository

**Updated:** 2025-11-21  
**Review Cycle:** Quarterly or after security incidents

---

### `article_7_authorized_signers.md`
**Purpose:** Legal authorization for document signing

**Key Sections:**
- Authorized signers for DAO LLC documents
- Legal authority and scope
- Signature verification process

**Use Case:** Compliance with Wyoming DAO LLC requirements

**Updated:** Previously created  
**Review Cycle:** Annually or when signers change

---

## 🔗 Related Documentation

These governance files work together with:

- **[AGENT_AUTHORIZATION_MODEL.md](../AGENT_AUTHORIZATION_MODEL.md)** - Comprehensive guide to agent permissions
- **[SECURITY.md](../SECURITY.md)** - Overall security policy including agent security
- **[VAULT_SECURITY_PLAYBOOK.md](../VAULT_SECURITY_PLAYBOOK.md)** - Secrets management
- **[.github/CODEOWNERS](../.github/CODEOWNERS)** - Code review requirements
- **[.github/BRANCH_PROTECTION_SETUP.md](../.github/BRANCH_PROTECTION_SETUP.md)** - Branch protection configuration

---

## 🎯 Governance Principles

### 1. Explicit Over Implicit
All permissions and authorities are explicitly documented. If it's not written here, it's not allowed.

### 2. Human-in-the-Loop
Critical decisions (legal, financial, production deployments) always require human review and approval.

### 3. Least Privilege
All actors (humans and agents) have the minimum permissions needed to perform their role.

### 4. Audit Everything
All actions with governance implications are logged, tracked, and auditable.

### 5. Regular Review
Governance policies are reviewed quarterly and updated as the organization evolves.

---

## 🔄 Review Process

### Quarterly Review Checklist

- [ ] Review all YAML files for accuracy
- [ ] Verify GitHub settings match documented policies
- [ ] Audit recent agent activity for violations
- [ ] Update authorized signers if team changed
- [ ] Check for new governance needs
- [ ] Document any incidents or exceptions
- [ ] Update review date in each file

**Last Review:** 2025-11-21  
**Next Review:** 2026-02-21  
**Reviewer:** Domenic Garza

---

## 📝 Making Changes to Governance

### For Access Matrix Changes (`access_matrix.yaml`)

1. **Propose change:** Open PR with updated file
2. **Justify:** Explain why the change is needed
3. **Review:** Requires approval from managing member
4. **Document:** Update this README if needed
5. **Communicate:** Notify affected parties

### For Agent Permission Changes (`agent_permissions.yaml`)

1. **Open issue:** Tag as `agent-permission-request`
2. **Discuss:** Team reviews in Discord #agents
3. **Consensus:** Requires agreement from admins
4. **PR:** Update the file with documented rationale
5. **Monitor:** Review impact after 30 days
6. **Revoke:** If unused or problematic, remove permission

### For Signer Authorization Changes (`article_7_authorized_signers.md`)

1. **Legal review:** Consult with WY-licensed attorney
2. **Documentation:** Update with new signer info
3. **Notification:** File with Wyoming Secretary of State if required
4. **Communication:** Notify all stakeholders
5. **Verification:** Update signature verification process

---

## 🚨 Emergency Governance Actions

In case of security incident or governance violation:

### Immediate Actions
1. **Suspend access** for affected parties
2. **Alert team** via Discord #alerts
3. **Document incident** with timestamp and details
4. **Assess impact** and blast radius

### Investigation
1. **Review audit logs** for full timeline
2. **Identify root cause** of policy violation
3. **Determine if malicious** or accidental

### Remediation
1. **Fix vulnerability** or process gap
2. **Update policies** to prevent recurrence
3. **Restore access** if appropriate
4. **Communicate lessons** learned

### Documentation
1. **Create postmortem** document
2. **Update relevant policy** files
3. **Share with team** for transparency

---

## 📞 Contact & Questions

### For Governance Questions
- **Discord:** #governance channel (if exists) or #agents
- **Email:** admin@strategickhaos.com
- **GitHub:** Open issue with tag `governance`

### For Access Requests
- **Process:** Follow process documented in relevant YAML file
- **Escalation:** Contact @Strategickhaos on Discord

### For Legal Questions
- **Contact:** Wyoming-licensed attorney (as referenced in `access_matrix.yaml`)
- **Scope:** Legal documents, signing authority, compliance

---

## 🔐 Security Note

These governance files are:
- ✅ **Public** - Transparency is a feature, not a bug
- ✅ **Version controlled** - All changes are tracked
- ✅ **Protected** - Changes require CODEOWNERS approval
- ❌ **NOT for secrets** - Never put keys, tokens, or credentials here

**See:** [SECURITY.md](../SECURITY.md) for secrets management policy

---

## 📚 References

### Internal
- [Community Manifesto](../COMMUNITY.md)
- [Contributors Guide](../CONTRIBUTORS.md)
- [Architecture Overview](../README.md)

### External
- [Wyoming DAO LLC Statute](https://www.wyoleg.gov/Legislation/2021/HB0062)
- [GitHub Governance Best Practices](https://docs.github.com/en/organizations)
- [CNCF Governance Principles](https://github.com/cncf/foundation/blob/main/charter.md)

---

## 🎓 Governance Philosophy

At Strategickhaos, governance is not about control—it's about **clarity and consent**.

We document:
- What everyone can do (permissions)
- What processes we follow (workflows)
- What principles guide us (values)
- What happens when things go wrong (incident response)

We believe:
- **Transparency** builds trust
- **Explicit rules** prevent conflicts
- **Human judgment** is irreplaceable
- **Automation** serves humans, not the reverse

This governance model ensures agents are **powerful tools** in human hands, not autonomous actors with unchecked authority.

---

**Built with 🏛️ by Strategickhaos DAO LLC**  
*Sovereignty through explicit governance and transparent controls*
