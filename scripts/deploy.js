const hre = require("hardhat");
const fs = require("fs");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying from:", deployer.address);

  // Auto-load Merkle root
  const data = JSON.parse(fs.readFileSync("merkle-data.json", "utf8"));
  const root = data.root;
  console.log("Using Merkle Root:", root);

  const opsWallet = deployer.address; // Replace with real multisig later

  // Deploy Distributor
  const Distributor = await hre.ethers.getContractFactory("MerkleDistributor");
  const distributor = await Distributor.deploy(root);
  await distributor.waitForDeployment();
  console.log("MerkleDistributor (7% vault):", await distributor.getAddress());

  // Deploy Splitter
  const Splitter = await hre.ethers.getContractFactory("CharitySplitter");
  const splitter = await Splitter.deploy(opsWallet, await distributor.getAddress());
  await splitter.waitForDeployment();
  console.log("CharitySplitter (93→7 gateway):", await splitter.getAddress());

  console.log("\n7% CHARITY SINK IS NOW ETERNAL");
  console.log("https://sepolia.basescan.org/address/" + await splitter.getAddress());
}

main().catch(err => { console.error(err); process.exit(1); });
