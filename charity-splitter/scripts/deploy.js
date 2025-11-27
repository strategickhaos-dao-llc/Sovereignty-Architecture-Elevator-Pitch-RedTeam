const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);

  // 1. Deploy MerkleDistributor
  // ⚠️ IMPORTANT: PLACEHOLDER MERKLE ROOT - DO NOT USE IN PRODUCTION!
  // Before mainnet deployment, generate the actual Merkle root from your charity list:
  // - St. Jude's Children's Research Hospital
  // - Médecins Sans Frontières  
  // - Veteran support programs
  // Use a Merkle tree library to compute the root from (index, address, amount) tuples
  const MOCK_ROOT = "0x0000000000000000000000000000000000000000000000000000000000000000"; 
  const MerkleDistributor = await hre.ethers.getContractFactory("MerkleDistributor");
  const distributor = await MerkleDistributor.deploy(MOCK_ROOT);
  await distributor.waitForDeployment();
  
  const distributorAddress = await distributor.getAddress();
  console.log("MerkleDistributor deployed to:", distributorAddress);

  // 2. Deploy CharitySplitter
  // ⚠️ IMPORTANT: PLACEHOLDER OPS WALLET - DO NOT USE IN PRODUCTION!
  // Before mainnet deployment, replace with your actual Ops Multisig address
  // (e.g., a Gnosis Safe multisig for operational fund management)
  const OPS_WALLET = deployer.address;
  
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
