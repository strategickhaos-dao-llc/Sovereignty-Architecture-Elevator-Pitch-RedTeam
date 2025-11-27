const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

/**
 * SwarmGate v1.0 — Deployment Script
 * 
 * Deploys:
 * 1. MerkleDistributor (with Merkle root for charity beneficiaries)
 * 2. CharitySplitter (93/7 split between ops and charity)
 */

async function main() {
  console.log("\n🚀 SwarmGate v1.0 — Deployment\n");
  console.log("Network:", hre.network.name);
  console.log("─".repeat(60));

  const [deployer] = await hre.ethers.getSigners();
  console.log("Deployer:", deployer.address);
  console.log("Balance:", hre.ethers.formatEther(await hre.ethers.provider.getBalance(deployer.address)), "ETH\n");

  // Load Merkle root (or use placeholder for testing)
  let merkleRoot = "0x" + "0".repeat(64);
  const merkleRootPath = path.join(__dirname, "..", "merkle-root.json");
  
  if (fs.existsSync(merkleRootPath)) {
    const merkleData = JSON.parse(fs.readFileSync(merkleRootPath, "utf8"));
    merkleRoot = merkleData.root;
    console.log("📄 Loaded Merkle root from file:", merkleRoot);
  } else {
    console.log("⚠️  No merkle-root.json found, using placeholder root");
    console.log("   Run 'npm run generate-root' to create one first");
  }

  // Configuration
  const OPS_WALLET = process.env.OPS_WALLET || deployer.address;
  console.log("\nConfiguration:");
  console.log("  Ops Wallet:", OPS_WALLET);
  console.log("  Merkle Root:", merkleRoot);
  console.log("─".repeat(60));

  // Deploy MerkleDistributor
  console.log("\n1️⃣  Deploying MerkleDistributor...");
  const MerkleDistributor = await hre.ethers.getContractFactory("MerkleDistributor");
  const distributor = await MerkleDistributor.deploy(merkleRoot);
  await distributor.waitForDeployment();
  const distributorAddress = await distributor.getAddress();
  console.log("   ✅ MerkleDistributor deployed to:", distributorAddress);

  // Deploy CharitySplitter
  console.log("\n2️⃣  Deploying CharitySplitter...");
  const CharitySplitter = await hre.ethers.getContractFactory("CharitySplitter");
  const splitter = await CharitySplitter.deploy(OPS_WALLET, distributorAddress);
  await splitter.waitForDeployment();
  const splitterAddress = await splitter.getAddress();
  console.log("   ✅ CharitySplitter deployed to:", splitterAddress);

  // Summary
  console.log("\n" + "═".repeat(60));
  console.log("🎉 DEPLOYMENT COMPLETE");
  console.log("═".repeat(60));
  console.log("\nContract Addresses:");
  console.log("  MerkleDistributor:", distributorAddress);
  console.log("  CharitySplitter:  ", splitterAddress);
  console.log("\nSplit Configuration:");
  console.log("  Operations (93%):", OPS_WALLET);
  console.log("  Charity (7%):    ", distributorAddress);
  console.log("\n💡 Send ETH to CharitySplitter address to trigger the 93/7 split.");
  console.log("═".repeat(60));

  // Save deployment info
  const deploymentInfo = {
    network: hre.network.name,
    deployer: deployer.address,
    contracts: {
      MerkleDistributor: distributorAddress,
      CharitySplitter: splitterAddress,
    },
    configuration: {
      opsWallet: OPS_WALLET,
      merkleRoot,
    },
    deployedAt: new Date().toISOString(),
  };

  const deploymentPath = path.join(__dirname, "..", `deployment-${hre.network.name}.json`);
  fs.writeFileSync(deploymentPath, JSON.stringify(deploymentInfo, null, 2));
  console.log(`\n📄 Deployment info saved to: ${deploymentPath}\n`);

  return deploymentInfo;
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
