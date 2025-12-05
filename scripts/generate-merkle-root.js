const { MerkleTree } = require("merkletreejs");
const keccak256 = require("keccak256");
const { ethers } = require("ethers");
const fs = require("fs");
const path = require("path");

/**
 * SwarmGate v1.0 — Merkle Root Generator
 * 
 * Configure your charity beneficiaries and their allocations below.
 * Each beneficiary gets a percentage of the 7% charity allocation.
 */

// ============================================
// ⚠️  WARNING: EDIT THESE ADDRESSES BEFORE MAINNET DEPLOYMENT
// ⚠️  These placeholder addresses are for testing only.
// ⚠️  Using placeholder addresses in production will result in
// ⚠️  funds being sent to uncontrolled addresses!
// ============================================
const beneficiaries = [
  {
    name: "St. Jude's Children's Research Hospital",
    address: "0x0000000000000000000000000000000000000001", // ⚠️ REPLACE WITH REAL ADDRESS BEFORE MAINNET
    allocation: ethers.parseEther("0.033"), // ~33% of 7% = ~2.33% of total
  },
  {
    name: "Médecins Sans Frontières",
    address: "0x0000000000000000000000000000000000000002", // ⚠️ REPLACE WITH REAL ADDRESS BEFORE MAINNET
    allocation: ethers.parseEther("0.033"), // ~33% of 7% = ~2.33% of total
  },
  {
    name: "Veteran Support Programs",
    address: "0x0000000000000000000000000000000000000003", // ⚠️ REPLACE WITH REAL ADDRESS BEFORE MAINNET
    allocation: ethers.parseEther("0.034"), // ~34% of 7% = ~2.34% of total
  },
];

function generateMerkleRoot() {
  console.log("\n🌳 SwarmGate v1.0 — Merkle Root Generator\n");
  console.log("Beneficiaries:");
  console.log("─".repeat(60));

  const leaves = beneficiaries.map((b) => {
    console.log(`  • ${b.name}`);
    console.log(`    Address: ${b.address}`);
    console.log(`    Allocation: ${ethers.formatEther(b.allocation)} ETH`);
    console.log();

    // Create leaf: keccak256(abi.encodePacked(address, amount))
    return keccak256(
      Buffer.concat([
        Buffer.from(b.address.slice(2).padStart(64, "0"), "hex"),
        Buffer.from(b.allocation.toString(16).padStart(64, "0"), "hex"),
      ])
    );
  });

  const tree = new MerkleTree(leaves, keccak256, { sortPairs: true });
  const root = tree.getHexRoot();

  console.log("─".repeat(60));
  console.log(`\n✅ Merkle Root: ${root}\n`);

  // Save to file for deployment
  const outputPath = path.join(__dirname, "..", "merkle-root.json");
  const output = {
    root,
    beneficiaries: beneficiaries.map((b) => ({
      name: b.name,
      address: b.address,
      allocation: b.allocation.toString(),
    })),
    generatedAt: new Date().toISOString(),
  };

  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));
  console.log(`📄 Saved to: ${outputPath}\n`);

  // Generate proofs for each beneficiary
  console.log("Proofs for claiming:");
  console.log("─".repeat(60));
  beneficiaries.forEach((b, i) => {
    const proof = tree.getHexProof(leaves[i]);
    console.log(`\n${b.name}:`);
    console.log(`  Proof: ${JSON.stringify(proof)}`);
  });

  console.log("\n─".repeat(60));
  console.log("✅ Done! Use this root in your MerkleDistributor deployment.\n");

  return root;
}

// Run if called directly
if (require.main === module) {
  generateMerkleRoot();
}

module.exports = { generateMerkleRoot, beneficiaries };
