# Branch Protection Setup Guide

This guide walks you through configuring GitHub branch protection rules to enforce the agent authorization model.

---

## 🎯 Why Branch Protection?

Branch protection ensures:
- Agents cannot push directly to protected branches
- All changes go through PR review process
- Critical files require CODEOWNERS approval
- Automated tests must pass before merge
- Production deployments are controlled

---

## 🔧 Configuration Steps

### 1. Navigate to Branch Protection Settings

1. Go to your repository on GitHub
2. Click **Settings** → **Branches**
3. Under "Branch protection rules", click **Add rule**

### 2. Protect `main` Branch

**Branch name pattern:** `main`

**Required settings:**

✅ **Require a pull request before merging**
- Required approving reviews: **1**
- Dismiss stale pull request approvals when new commits are pushed: **✓**
- Require review from Code Owners: **✓**

✅ **Require status checks to pass before merging**
- Require branches to be up to date before merging: **✓**
- Status checks that are required:
  - `Agent PR Validation / Validate Agent PR Compliance`
  - `Build and Test / build-and-test`
  - `Security Scan / security-scan`

✅ **Require conversation resolution before merging**

✅ **Require signed commits** (optional but recommended)

✅ **Require linear history** (optional but recommended)

✅ **Include administrators** (recommended)
- Enforces all rules on repository admins too

❌ **Allow force pushes** - MUST BE DISABLED

❌ **Allow deletions** - MUST BE DISABLED

**Screenshot reference:**
```
Branch protection rule
┌─────────────────────────────────────────────┐
│ Branch name pattern: main                   │
├─────────────────────────────────────────────┤
│ ☑ Require a pull request before merging    │
│   • Required approving reviews: 1           │
│   ☑ Dismiss stale pull request approvals   │
│   ☑ Require review from Code Owners        │
│                                             │
│ ☑ Require status checks to pass            │
│   ☑ Require branches to be up to date      │
│   • Agent PR Validation                     │
│   • Build and Test                          │
│   • Security Scan                           │
│                                             │
│ ☑ Require conversation resolution          │
│ ☑ Require signed commits                   │
│ ☑ Require linear history                   │
│ ☑ Include administrators                   │
│ ☐ Allow force pushes                       │
│ ☐ Allow deletions                          │
└─────────────────────────────────────────────┘
```

### 3. Protect `develop` Branch

**Branch name pattern:** `develop`

Same settings as `main`, but slightly relaxed:

✅ **Require a pull request before merging**
- Required approving reviews: **1**
- Dismiss stale pull request approvals: **✓**
- Require review from Code Owners: **✓** (for critical files only)

✅ **Require status checks to pass before merging**
- Same status checks as `main`

✅ **Require conversation resolution before merging**

❌ **Allow force pushes** - DISABLED

❌ **Allow deletions** - DISABLED

### 4. Protect Release Branches

**Branch name pattern:** `release/*`

Same settings as `main` - production-grade protection.

---

## 🔐 GitHub Environments Setup

Environments provide an additional layer of protection for deployments.

### Create Environments

1. Go to **Settings** → **Environments**
2. Click **New environment**

### Development Environment

**Name:** `dev`

**Protection rules:**
- No protection rules (auto-deploy is OK)

**Environment secrets:**
- `DEV_KUBECONFIG` (if using K8s auto-deploy)

**Deployment branches:**
- Selected branches: `develop`

### Staging Environment

**Name:** `staging`

**Protection rules:**
- Wait timer: **2 minutes**
- Required reviewers: (optional)

**Environment secrets:**
- `STAGING_KUBECONFIG`

**Deployment branches:**
- Selected branches: `main`, `develop`

### Production Environment

**Name:** `production`

**Protection rules:**
- Required reviewers: **@Strategickhaos** (or your admin team)
- Wait timer: **5 minutes**

**Environment secrets:**
- `PROD_KUBECONFIG`
- `PROD_API_KEYS` (if needed)

**Deployment branches:**
- Selected branches: `main` only

---

## 📋 CODEOWNERS Configuration

The `.github/CODEOWNERS` file has been created. To enable it:

1. Ensure branch protection has **"Require review from Code Owners"** enabled
2. Verify your GitHub username matches the one in `CODEOWNERS`
3. Update `CODEOWNERS` with your actual team/user handles

**Example:**
```
# Replace @Strategickhaos with actual GitHub username or team
/bootstrap/k8s/ @Strategickhaos
/.github/workflows/ @Strategickhaos
/SECURITY.md @Strategickhaos
```

**To use a team instead of individual:**
```
/bootstrap/k8s/ @strategickhaos-swarm-intelligence/platform-team
```

---

## ✅ Verification Checklist

After configuration, verify the setup:

### Test 1: Agent Cannot Push to Main
```bash
# This should fail:
git checkout main
git commit --allow-empty -m "Test direct push"
git push origin main
# Expected: "protected branch hook declined"
```

### Test 2: PR Required
```bash
# This should work:
git checkout -b copilot/test-branch-protection
git commit --allow-empty -m "Test PR workflow"
git push origin copilot/test-branch-protection
# Open PR on GitHub - should be able to create PR
# Should NOT be able to merge without review
```

### Test 3: Status Checks Required
- Open a PR
- Make a change that fails tests
- Verify PR cannot be merged until tests pass

### Test 4: CODEOWNERS Review Required
```bash
# Create a PR that modifies a CODEOWNERS-protected file
git checkout -b test-codeowners
echo "# test" >> bootstrap/k8s/rbac.yaml
git add bootstrap/k8s/rbac.yaml
git commit -m "Test CODEOWNERS"
git push origin test-codeowners
# Open PR - should require review from @Strategickhaos
```

### Test 5: Production Environment Protection
- Go to **Actions** tab
- Run "Deployment with Environment Gates" workflow
- Select "production" environment
- Verify approval is required before deployment proceeds

---

## 🚨 Troubleshooting

### "I can't push to main even though I'm an admin"

**Solution:** This is correct behavior if "Include administrators" is enabled. Use PR workflow instead.

### "Status checks are not appearing"

**Solution:**
1. Ensure workflows have run at least once to register status checks
2. Check workflow file names match exactly
3. Wait a few minutes for GitHub to refresh

### "CODEOWNERS review not required"

**Solution:**
1. Verify "Require review from Code Owners" is checked in branch protection
2. Verify CODEOWNERS file is in `.github/CODEOWNERS`
3. Verify GitHub usernames/teams in CODEOWNERS exist
4. Re-save branch protection rules

### "Environment protection not working"

**Solution:**
1. Verify environment name in workflow matches exactly (case-sensitive)
2. Verify deployment branches are configured
3. Check that workflow uses `environment:` key correctly

---

## 📚 Additional Resources

- [GitHub Branch Protection Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [GitHub Environments Docs](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [CODEOWNERS Docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

---

## 🔄 Maintenance

Review and update branch protection rules:

- **Quarterly:** Verify rules match current needs
- **After incidents:** Strengthen rules if needed
- **When adding new workflows:** Add required status checks
- **When team changes:** Update CODEOWNERS

**Last Updated:** 2025-11-21  
**Next Review:** 2026-02-21

---

**Need Help?** Contact @Strategickhaos in Discord #agents channel
