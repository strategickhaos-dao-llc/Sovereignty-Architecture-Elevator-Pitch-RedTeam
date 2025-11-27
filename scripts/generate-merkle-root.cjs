/**
 * @title Merkle Root Generator for Charity Distribution
 * @notice Generates Merkle tree and proofs for charity claims
 * @dev Run with: npm run generate-root
 * 
 * Strategickhaos DAO - 7% Charity Splitter
 * This script creates the cryptographic proofs needed for charities to claim funds
 */

const { MerkleTree } = require("merkletreejs");
const keccak256 = require("keccak256");
const { ethers } = require("hardhat");
const fs = require("fs");
const path = require("path");

// --- CHARITY CONFIGURATION ---
// Replace these with REAL charity addresses and their allocations
// Total amount should equal the expected 7% charity pool
const charities = [
  {
    name: "St. Jude Children's Research Hospital",
    address: "0x5555555555555555555555555555555555555555", // Replace with real address
    amount: ethers.parseEther("1.5"), // 1.5 ETH allocation
  },
  {
    name: "Médecins Sans Frontières (Doctors Without Borders)",
    address: "0x6666666666666666666666666666666666666666", // Replace with real address
    amount: ethers.parseEther("1.5"), // 1.5 ETH allocation
  },
  {
    name: "Veterans Support Foundation",
    address: "0x7777777777777777777777777777777777777777", // Replace with real address
    amount: ethers.parseEther("0.5"), // 0.5 ETH allocation
  },
];

/**
 * Generate leaf node for Merkle tree
 * @param index Unique index for the claim
 * @param address Recipient address
 * @param amount Amount in wei
 * @returns Keccak256 hash of packed data
 */
function generateLeaf(index, address, amount) {
  return Buffer.from(
    ethers.solidityPackedKeccak256(
      ["uint256", "address", "uint256"],
      [index, address, amount]
    ).slice(2),
    "hex"
  );
}

async function main() {
  console.log("🌳 Strategickhaos Charity Merkle Tree Generator");
  console.log("================================================\n");

  console.log("📋 Charity Recipients:");
  let totalAllocation = BigInt(0);
  
  charities.forEach((charity, i) => {
    console.log(`   ${i + 1}. ${charity.name}`);
    console.log(`      Address: ${charity.address}`);
    console.log(`      Amount:  ${ethers.formatEther(charity.amount)} ETH\n`);
    totalAllocation += charity.amount;
  });

  console.log(`💰 Total Allocation: ${ethers.formatEther(totalAllocation)} ETH\n`);

  // Generate leaf nodes
  console.log("🔷 Generating Merkle tree leaves...");
  const leaves = charities.map((charity, index) => {
    return generateLeaf(index, charity.address, charity.amount);
  });

  // Create Merkle tree
  const tree = new MerkleTree(leaves, keccak256, { sortPairs: true });

  // Get root
  const root = tree.getHexRoot();
  console.log("\n✅ Merkle Root Generated:");
  console.log(`   ${root}\n`);

  // Generate proofs for each charity
  console.log("🔑 Generating proofs for each charity...\n");
  const proofs = charities.map((charity, index) => {
    const leaf = leaves[index];
    const proof = tree.getHexProof(leaf);
    
    return {
      index: index,
      name: charity.name,
      address: charity.address,
      amount: charity.amount.toString(),
      amountFormatted: ethers.formatEther(charity.amount) + " ETH",
      proof: proof,
      leaf: "0x" + leaf.toString("hex")
    };
  });

  // Display proofs
  proofs.forEach((p) => {
    console.log(`📜 Proof for ${p.name}:`);
    console.log(`   Index:   ${p.index}`);
    console.log(`   Address: ${p.address}`);
    console.log(`   Amount:  ${p.amountFormatted}`);
    console.log(`   Proof:   ${JSON.stringify(p.proof)}\n`);
  });

  // Save to file
  const outputData = {
    generated: new Date().toISOString(),
    network: "base-sepolia",
    root: root,
    totalAllocation: totalAllocation.toString(),
    totalAllocationFormatted: ethers.formatEther(totalAllocation) + " ETH",
    charityCount: charities.length,
    proofs: proofs
  };

  const outputPath = path.join(__dirname, "..", "merkle-data.json");
  fs.writeFileSync(outputPath, JSON.stringify(outputData, null, 2));
  
  console.log("================================================");
  console.log("✅ Merkle data saved to: merkle-data.json");
  console.log("\n📋 Next Steps:");
  console.log("   1. Update charity addresses in this script with real addresses");
  console.log("   2. Re-run this script to generate new proofs");
  console.log("   3. Deploy contracts with the new Merkle root");
  console.log("   4. Share proofs with respective charities");
  console.log("\n🔐 Contract Deployment:");
  console.log(`   Use this root when deploying MerkleDistributor:`);
  console.log(`   ${root}\n`);

  return { root, proofs };
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Error generating Merkle tree:", error);
    process.exit(1);
  });
