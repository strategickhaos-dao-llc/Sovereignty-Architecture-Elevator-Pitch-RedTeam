const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);

  // CONFIGURATION
  // ⚠️  IMPORTANT: Replace these with your real Safe/Multisig address before production deployment!
  const OPERATIONAL_MULTISIG = deployer.address; // Temporary: using deployer for demo
  
  // ⚠️  IMPORTANT: Replace these placeholder addresses with real charity wallet addresses before deployment!
  // Using placeholder addresses in production will result in LOSS OF FUNDS.
  // Example: St. Jude's, MSF (Doctors Without Borders), etc.
  const CHARITIES = [
    "0x0000000000000000000000000000000000000001", // Placeholder 1 - REPLACE BEFORE DEPLOYMENT
    "0x0000000000000000000000000000000000000002", // Placeholder 2 - REPLACE BEFORE DEPLOYMENT
    "0x0000000000000000000000000000000000000003"  // Placeholder 3 - REPLACE BEFORE DEPLOYMENT
  ];

  // Safety check for production deployments
  const isTestnet = hre.network.name === "hardhat" || hre.network.name === "localhost" || hre.network.name.includes("sepolia");
  if (!isTestnet) {
    // Check for placeholder addresses on mainnet
    const hasPlaceholder = CHARITIES.some(addr => addr.startsWith("0x000000000000000000000000000000000000000"));
    if (hasPlaceholder) {
      throw new Error("DEPLOYMENT BLOCKED: Replace placeholder charity addresses before mainnet deployment!");
    }
  }

  const CharitySplitter = await hre.ethers.getContractFactory("ImmutableCharitySplitter");
  const splitter = await CharitySplitter.deploy(OPERATIONAL_MULTISIG, CHARITIES);

  await splitter.waitForDeployment();

  console.log("ImmutableCharitySplitter deployed to:", await splitter.getAddress());
  console.log("Ops Multisig set to:", OPERATIONAL_MULTISIG);
  console.log("Charity Count:", CHARITIES.length);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
