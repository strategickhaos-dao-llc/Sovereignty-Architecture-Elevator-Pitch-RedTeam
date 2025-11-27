/**
 * @title Strategickhaos Charity Splitter - Deployment Script
 * @notice Deploys CharitySplitter and MerkleDistributor to Base Sepolia
 * @dev Run with: npx hardhat run scripts/deploy.cjs --network baseSepolia
 */

const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  console.log("🚀 Strategickhaos 7% Charity Splitter Deployment");
  console.log("================================================\n");

  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);
  
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", hre.ethers.formatEther(balance), "ETH\n");

  // Load configuration
  const opsWallet = process.env.OPS_WALLET_ADDRESS;
  if (!opsWallet) {
    throw new Error("OPS_WALLET_ADDRESS not set in environment");
  }

  // Load merkle root from generated file or use placeholder
  let merkleRoot;
  const merkleDataPath = path.join(__dirname, "..", "merkle-data.json");
  
  if (fs.existsSync(merkleDataPath)) {
    const merkleData = JSON.parse(fs.readFileSync(merkleDataPath, "utf8"));
    merkleRoot = merkleData.root;
    console.log("✅ Loaded Merkle root from merkle-data.json");
  } else {
    // Use a placeholder root for initial deployment (can be updated later)
    merkleRoot = "0x" + "0".repeat(64);
    console.log("⚠️  No merkle-data.json found, using placeholder root");
    console.log("   Run 'npm run generate-root' to create real Merkle tree");
  }

  console.log("\n📋 Deployment Configuration:");
  console.log("   Operations Wallet:", opsWallet);
  console.log("   Merkle Root:", merkleRoot.substring(0, 18) + "...");

  // Deploy MerkleDistributor first (charity wallet needs to exist)
  console.log("\n🔷 Deploying MerkleDistributor...");
  const MerkleDistributor = await hre.ethers.getContractFactory("MerkleDistributor");
  
  // Use a non-zero placeholder root if the generated one is all zeros
  const deployRoot = merkleRoot === "0x" + "0".repeat(64) 
    ? "0x" + "1".repeat(64) // Placeholder non-zero root
    : merkleRoot;
    
  const distributor = await MerkleDistributor.deploy(deployRoot);
  await distributor.waitForDeployment();
  const distributorAddress = await distributor.getAddress();
  console.log("   MerkleDistributor deployed to:", distributorAddress);

  // Deploy CharitySplitter
  console.log("\n🔷 Deploying CharitySplitter...");
  const CharitySplitter = await hre.ethers.getContractFactory("CharitySplitter");
  const splitter = await CharitySplitter.deploy(opsWallet, distributorAddress);
  await splitter.waitForDeployment();
  const splitterAddress = await splitter.getAddress();
  console.log("   CharitySplitter deployed to:", splitterAddress);

  // Verify deployment
  console.log("\n✅ Deployment Complete!");
  console.log("================================================");
  console.log("\n📝 Contract Addresses:");
  console.log(`   CharitySplitter:    ${splitterAddress}`);
  console.log(`   MerkleDistributor:  ${distributorAddress}`);
  
  console.log("\n💰 Fund Split Configuration:");
  console.log("   Operations (93%):  ", opsWallet);
  console.log("   Charity (7%):      ", distributorAddress);

  // Save deployment info
  const deploymentInfo = {
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    contracts: {
      CharitySplitter: splitterAddress,
      MerkleDistributor: distributorAddress
    },
    configuration: {
      opsWallet: opsWallet,
      merkleRoot: deployRoot,
      charityBps: 700
    }
  };

  const deploymentPath = path.join(__dirname, "..", "deployment.json");
  fs.writeFileSync(deploymentPath, JSON.stringify(deploymentInfo, null, 2));
  console.log("\n📁 Deployment info saved to deployment.json");

  // Verification instructions
  console.log("\n🔍 To verify contracts on BaseScan:");
  console.log(`   npx hardhat verify --network baseSepolia ${distributorAddress} "${deployRoot}"`);
  console.log(`   npx hardhat verify --network baseSepolia ${splitterAddress} "${opsWallet}" "${distributorAddress}"`);

  console.log("\n🎯 Next Steps:");
  console.log("   1. Send test ETH to CharitySplitter:", splitterAddress);
  console.log("   2. Verify 93% goes to ops, 7% to distributor");
  console.log("   3. Update merkle root with real charity addresses");
  console.log("   4. Charities can claim using their proofs\n");

  return deploymentInfo;
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Deployment failed:", error);
    process.exit(1);
  });
