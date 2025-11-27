// SwarmGate v1.0 - Deployment Script
// Deploys CharitySplitter and MerkleDistributor to Base network
// Author: Strategickhaos DAO LLC / ValorYield Engine

const hre = require("hardhat");

async function main() {
  console.log("🚀 SwarmGate v1.0 Deployment Starting...\n");

  const [deployer] = await hre.ethers.getSigners();
  console.log("📍 Deploying contracts with account:", deployer.address);
  
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("💰 Account balance:", hre.ethers.formatEther(balance), "ETH\n");

  // Configuration - Update these addresses before mainnet deployment
  // For testnet, we'll use placeholder addresses that can be updated later
  const CHARITY_POOL = process.env.CHARITY_POOL_ADDRESS || deployer.address;
  const TREASURY = process.env.TREASURY_ADDRESS || deployer.address;

  console.log("📋 Configuration:");
  console.log("   Charity Pool:", CHARITY_POOL);
  console.log("   Treasury:", TREASURY);
  console.log("");

  // Deploy CharitySplitter
  console.log("📦 Deploying CharitySplitter...");
  const CharitySplitter = await hre.ethers.getContractFactory("CharitySplitter");
  const charitySplitter = await CharitySplitter.deploy(CHARITY_POOL, TREASURY);
  await charitySplitter.waitForDeployment();
  
  const charitySplitterAddress = await charitySplitter.getAddress();
  console.log("✅ CharitySplitter deployed to:", charitySplitterAddress);

  // Deploy MerkleDistributor
  console.log("\n📦 Deploying MerkleDistributor...");
  const MerkleDistributor = await hre.ethers.getContractFactory("MerkleDistributor");
  const merkleDistributor = await MerkleDistributor.deploy();
  await merkleDistributor.waitForDeployment();
  
  const merkleDistributorAddress = await merkleDistributor.getAddress();
  console.log("✅ MerkleDistributor deployed to:", merkleDistributorAddress);

  // Deployment summary
  console.log("\n" + "=".repeat(60));
  console.log("🎉 SwarmGate v1.0 Deployment Complete!");
  console.log("=".repeat(60));
  console.log("\n📜 Contract Addresses:");
  console.log("   CharitySplitter:", charitySplitterAddress);
  console.log("   MerkleDistributor:", merkleDistributorAddress);
  console.log("\n🔗 Network:", hre.network.name);
  console.log("🔗 Chain ID:", (await hre.ethers.provider.getNetwork()).chainId.toString());

  // Verification instructions
  console.log("\n📝 To verify contracts on Basescan:");
  console.log(`   npx hardhat verify --network ${hre.network.name} ${charitySplitterAddress} "${CHARITY_POOL}" "${TREASURY}"`);
  console.log(`   npx hardhat verify --network ${hre.network.name} ${merkleDistributorAddress}`);

  // Return addresses for programmatic use
  return {
    charitySplitter: charitySplitterAddress,
    merkleDistributor: merkleDistributorAddress,
    network: hre.network.name,
    deployer: deployer.address,
  };
}

main()
  .then((result) => {
    console.log("\n✨ Deployment script completed successfully");
    process.exit(0);
  })
  .catch((error) => {
    console.error("\n❌ Deployment failed:", error);
    process.exit(1);
  });
