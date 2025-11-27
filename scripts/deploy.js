/**
 * SwarmGate v1.0 - Deployment Script
 *
 * Deploys CharitySplitter and MerkleDistributor contracts.
 *
 * Usage:
 *   npm run deploy              # Local hardhat network
 *   npm run deploy:base-sepolia # Base Sepolia testnet
 *   npm run deploy:base         # Base mainnet (production)
 */

const { ethers, network } = require("hardhat");
const fs = require("fs");
const path = require("path");

// EDIT THESE: Your operations wallet address
const OPS_WALLET = process.env.OPS_WALLET || "0x0000000000000000000000000000000000000000";

async function main() {
  console.log("🚀 SwarmGate v1.0 - Deployment Script\n");
  console.log(`📡 Network: ${network.name}`);

  const [deployer] = await ethers.getSigners();
  console.log(`🔑 Deployer: ${deployer.address}`);

  const balance = await ethers.provider.getBalance(deployer.address);
  console.log(`💰 Balance: ${ethers.formatEther(balance)} ETH\n`);

  // Load merkle root from generated file
  let merkleRoot = "0x" + "0".repeat(64); // Default empty root
  const merkleTreePath = path.join(__dirname, "..", "merkle-tree.json");

  if (fs.existsSync(merkleTreePath)) {
    const treeData = JSON.parse(fs.readFileSync(merkleTreePath, "utf8"));
    merkleRoot = treeData.root;
    console.log(`📊 Using Merkle Root from file: ${merkleRoot}`);
  } else {
    console.log("⚠️  No merkle-tree.json found. Using empty merkle root.");
    console.log("   Run 'npm run generate-root' first for production deployment.");
  }

  // Validate ops wallet
  if (OPS_WALLET === "0x0000000000000000000000000000000000000000") {
    console.log("\n⚠️  WARNING: Using zero address as ops wallet!");
    console.log("   Set OPS_WALLET environment variable for production.\n");
  } else {
    console.log(`🏢 Ops Wallet: ${OPS_WALLET}`);
  }

  // Deploy MerkleDistributor
  console.log("\n📦 Deploying MerkleDistributor...");
  const Distributor = await ethers.getContractFactory("MerkleDistributor");
  const distributor = await Distributor.deploy(merkleRoot);
  await distributor.waitForDeployment();
  const distributorAddress = await distributor.getAddress();
  console.log(`✅ MerkleDistributor deployed at: ${distributorAddress}`);

  // Deploy CharitySplitter
  console.log("\n📦 Deploying CharitySplitter...");
  const Splitter = await ethers.getContractFactory("CharitySplitter");
  const splitter = await Splitter.deploy(OPS_WALLET, distributorAddress);
  await splitter.waitForDeployment();
  const splitterAddress = await splitter.getAddress();
  console.log(`✅ CharitySplitter deployed at: ${splitterAddress}`);

  // Summary
  console.log("\n" + "=".repeat(60));
  console.log("🎉 SwarmGate v1.0 Deployment Complete!");
  console.log("=".repeat(60));
  console.log(`
📋 Contract Addresses:
   CharitySplitter:    ${splitterAddress}
   MerkleDistributor:  ${distributorAddress}

💸 Split Configuration:
   Operations (93%):   ${OPS_WALLET}
   Charity (7%):       ${distributorAddress}

📝 Next Steps:
   1. Verify contracts on Basescan
   2. Update SWARMGATE_v1.0_STATUS.yaml with deployed addresses
   3. Send ETH to CharitySplitter address to test the split

🔗 Verification Commands:
   npx hardhat verify --network ${network.name} ${distributorAddress} "${merkleRoot}"
   npx hardhat verify --network ${network.name} ${splitterAddress} "${OPS_WALLET}" "${distributorAddress}"
`);

  // Save deployment info
  const deploymentInfo = {
    network: network.name,
    chainId: network.config.chainId,
    timestamp: new Date().toISOString(),
    deployer: deployer.address,
    contracts: {
      CharitySplitter: splitterAddress,
      MerkleDistributor: distributorAddress
    },
    configuration: {
      opsWallet: OPS_WALLET,
      merkleRoot: merkleRoot,
      opsShare: "93%",
      charityShare: "7%"
    }
  };

  const deploymentPath = path.join(__dirname, "..", `deployment-${network.name}.json`);
  fs.writeFileSync(deploymentPath, JSON.stringify(deploymentInfo, null, 2));
  console.log(`💾 Deployment info saved to: ${deploymentPath}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
