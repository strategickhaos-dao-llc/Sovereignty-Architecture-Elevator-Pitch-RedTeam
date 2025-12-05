/**
 * SwarmGate v1.0 - Merkle Root Generator
 *
 * Generates merkle roots for charity distribution.
 *
 * Usage:
 *   npm run generate-root
 *
 * Edit the CHARITY_RECIPIENTS below with real addresses and allocations.
 */

const { StandardMerkleTree } = require("@openzeppelin/merkle-tree");
const fs = require("fs");
const path = require("path");

// EDIT THESE: Real charity addresses and their allocations (in wei)
// Format: [index, address, amount]
const CHARITY_RECIPIENTS = [
  // Example: [0, "0xCharityAddress1", "1000000000000000000"], // 1 ETH
  // Example: [1, "0xCharityAddress2", "500000000000000000"],  // 0.5 ETH
  [0, "0x0000000000000000000000000000000000000001", "1000000000000000000"],
  [1, "0x0000000000000000000000000000000000000002", "500000000000000000"],
];

async function main() {
  console.log("🌳 SwarmGate v1.0 - Merkle Root Generator\n");

  if (CHARITY_RECIPIENTS.length === 0) {
    console.error("❌ No charity recipients defined. Edit CHARITY_RECIPIENTS in this file.");
    process.exit(1);
  }

  // Build the merkle tree
  // Leaves are: [index, account, amount]
  const tree = StandardMerkleTree.of(CHARITY_RECIPIENTS, ["uint256", "address", "uint256"]);

  console.log("📊 Merkle Root:", tree.root);
  console.log("📋 Recipients:", CHARITY_RECIPIENTS.length);

  // Save tree data for later proof generation
  const outputPath = path.join(__dirname, "..", "merkle-tree.json");
  fs.writeFileSync(outputPath, JSON.stringify({
    root: tree.root,
    recipients: CHARITY_RECIPIENTS,
    tree: tree.dump()
  }, null, 2));

  console.log(`\n✅ Merkle tree saved to ${outputPath}`);
  console.log("\n📝 Use this root when deploying MerkleDistributor:");
  console.log(`   ${tree.root}`);

  // Generate proofs for verification
  console.log("\n📜 Individual proofs:");
  for (const [i, v] of tree.entries()) {
    const proof = tree.getProof(i);
    console.log(`   ${v[0]}: ${v[1]} → ${v[2]} wei`);
    console.log(`      Proof: ${JSON.stringify(proof)}`);
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
