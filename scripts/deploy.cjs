const hre = require("hardhat");

async function main() {
  // SETUP: Replace these with REAL addresses before mainnet deployment!
  // WARNING: Using placeholder address - deployment will fail until replaced with real Gnosis Safe address
  const OPS_WALLET = "0x0000000000000000000000000000000000000000"; 
  
  // Example: St. Jude's, MSF, Wounded Warrior (Use real ETH addresses)
  // WARNING: Replace with verified charity wallet addresses before mainnet deployment
  const CHARITIES = [
    "0x0000000000000000000000000000000000000001", 
    "0x0000000000000000000000000000000000000002",
    "0x0000000000000000000000000000000000000003"
  ];

  // Validate configuration before deployment
  if (OPS_WALLET === "0x0000000000000000000000000000000000000000") {
    console.error("ERROR: OPS_WALLET is set to placeholder address. Update before deploying!");
    process.exitCode = 1;
    return;
  }

  console.log("Deploying SwarmGateSplitter...");
  console.log("Ops Wallet:", OPS_WALLET);
  console.log("Charities:", CHARITIES.length);

  const Splitter = await hre.ethers.getContractFactory("SwarmGateSplitter");
  const splitter = await Splitter.deploy(OPS_WALLET, CHARITIES);

  await splitter.waitForDeployment();

  console.log("SwarmGateSplitter deployed to:", await splitter.getAddress());
  console.log("Verify on block explorer: npx hardhat verify --network base ...", await splitter.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
