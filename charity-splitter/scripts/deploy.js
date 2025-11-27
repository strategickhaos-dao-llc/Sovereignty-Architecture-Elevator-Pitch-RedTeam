const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);

  // 1. Deploy MerkleDistributor
  // Example Root: 0x... (Replace with generated root of your charities)
  const MOCK_ROOT = "0x0000000000000000000000000000000000000000000000000000000000000000"; 
  const MerkleDistributor = await hre.ethers.getContractFactory("MerkleDistributor");
  const distributor = await MerkleDistributor.deploy(MOCK_ROOT);
  await distributor.waitForDeployment();
  
  const distributorAddress = await distributor.getAddress();
  console.log("MerkleDistributor deployed to:", distributorAddress);

  // 2. Deploy CharitySplitter
  // 93% receiver (Ops)
  const OPS_WALLET = deployer.address; // Replace with actual Ops Multisig
  
  const CharitySplitter = await hre.ethers.getContractFactory("CharitySplitter");
  const splitter = await CharitySplitter.deploy(OPS_WALLET, distributorAddress);
  await splitter.waitForDeployment();

  console.log("CharitySplitter deployed to:", await splitter.getAddress());
  console.log("Configuration:");
  console.log(" - Ops Wallet (93%):", OPS_WALLET);
  console.log(" - Distributor (7%):", distributorAddress);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
