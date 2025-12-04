const hre = require("hardhat");

async function main() {
  // ==========================================================================
  // CRITICAL: Replace these placeholder addresses before ANY deployment!
  // Using placeholder addresses will cause deployment failure or fund loss.
  // ==========================================================================
  
  // Ops Multisig: Replace with your Gnosis Safe or multisig address
  const OPS_WALLET = process.env.OPS_WALLET || "0xYourOpsMultisigAddressHere";
  
  // Charity Addresses: Replace with real charity wallet addresses
  // Example organizations: St. Jude's, MSF, Wounded Warrior Project
  const CHARITIES = process.env.CHARITIES 
    ? process.env.CHARITIES.split(",") 
    : [
        "0x0000000000000000000000000000000000000001", // Placeholder - REPLACE
        "0x0000000000000000000000000000000000000002", // Placeholder - REPLACE
        "0x0000000000000000000000000000000000000003"  // Placeholder - REPLACE
      ];

  // Validate addresses before deployment
  if (OPS_WALLET === "0xYourOpsMultisigAddressHere") {
    throw new Error("ERROR: OPS_WALLET must be set to a valid address before deployment!");
  }
  
  if (CHARITIES.some(addr => addr.startsWith("0x000000000000000000000000000000000000000"))) {
    throw new Error("ERROR: CHARITIES must be set to valid charity addresses before deployment!");
  }

  console.log("Deploying SwarmGateSplitter...");
  console.log("Ops Wallet:", OPS_WALLET);
  console.log("Charities:", CHARITIES.length, CHARITIES);

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
