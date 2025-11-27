const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", (await hre.ethers.provider.getBalance(deployer.address)).toString());

  // Operations wallet (deployer address by default)
  const OPS = deployer.address;

  // Charity addresses - replace with actual charity wallet addresses
  const CHARITIES = [
    "0x710F0568aA1b6f14a95d24486a1a1643b4E4E1Dc",
    "0x710F0568aA1b6f14a95d24486a1a1643b4E4E1Dc",
    "0x710F0568aA1b6f14a95d24486a1a1643b4E4E1Dc"
  ];

  console.log("Deploying SwarmGateSplitter...");
  console.log("OPS wallet:", OPS);
  console.log("Charity wallets:", CHARITIES);

  const SwarmGateSplitter = await hre.ethers.getContractFactory("SwarmGateSplitter");
  const splitter = await SwarmGateSplitter.deploy(OPS, CHARITIES);

  await splitter.waitForDeployment();

  const contractAddress = await splitter.getAddress();

  console.log("\n====================================");
  console.log("7% CHARITY SINK IS NOW ETERNAL");
  console.log("====================================");
  console.log("Contract deployed to:", contractAddress);
  console.log("Block explorer:", `https://sepolia.basescan.org/address/${contractAddress}`);
  console.log("\nContract configuration:");
  console.log("  - Charity allocation: 7% (700 basis points)");
  console.log("  - Operations allocation: 93%");
  console.log("  - Number of charities:", CHARITIES.length);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
