const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);

  // CONFIGURATION
  // Replace these with your real Safe/Multisig address
  const OPERATIONAL_MULTISIG = deployer.address; // Temporary: using deployer for demo
  
  // Replace with St. Jude's, MSF, etc. ETH addresses
  const CHARITIES = [
    "0x0000000000000000000000000000000000000001", // Placeholder 1
    "0x0000000000000000000000000000000000000002", // Placeholder 2
    "0x0000000000000000000000000000000000000003"  // Placeholder 3
  ];

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
