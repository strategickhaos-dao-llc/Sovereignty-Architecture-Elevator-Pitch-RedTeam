// scripts/validate-status.js

const fs = require("fs");
const path = require("path");
const yaml = require("js-yaml");

const STATUS_YAML = path.join(__dirname, "..", "SWARMGATE_v1.0_STATUS.yaml");

// Canonical expectations
const EXPECTED = {
  project: "SwarmGate",
  version: "v1.0",
  allocation: "7% irrevocable",
  blake3: "caa58d9faee9a10ce46d81d2f21e0da611ff962b8070e22b5d976cc816480698"
};

function fail(msg) {
  console.error(`[SWARMGATE STATUS VALIDATION] ❌ ${msg}`);
  process.exit(1);
}

function ok(msg) {
  console.log(`[SWARMGATE STATUS VALIDATION] ✅ ${msg}`);
}

function main() {
  if (!fs.existsSync(STATUS_YAML)) {
    fail(`Missing file: ${STATUS_YAML}`);
  }

  const raw = fs.readFileSync(STATUS_YAML, "utf8");
  let doc;
  try {
    doc = yaml.load(raw);
  } catch (e) {
    fail(`YAML parse error: ${e.message}`);
  }

  if (doc.project !== EXPECTED.project) {
    fail(`project mismatch: expected "${EXPECTED.project}", got "${doc.project}"`);
  }

  if (doc.version !== EXPECTED.version) {
    fail(`version mismatch: expected "${EXPECTED.version}", got "${doc.version}"`);
  }

  if (!doc.promise || doc.promise.allocation !== EXPECTED.allocation) {
    fail(
      `promise.allocation mismatch: expected "${EXPECTED.allocation}", got "${doc.promise && doc.promise.allocation}"`
    );
  }

  const actualHash =
    doc.canonical_hash && doc.canonical_hash.blake3
      ? String(doc.canonical_hash.blake3).toLowerCase()
      : null;

  if (actualHash !== EXPECTED.blake3) {
    fail(
      `canonical_hash.blake3 mismatch:\n  expected: ${EXPECTED.blake3}\n  got:      ${actualHash}`
    );
  }

  ok("SWARMGATE_v1.0_STATUS.yaml is valid and canonical.");
  process.exit(0);
}

main();
