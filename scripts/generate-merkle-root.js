const hre = require("hardhat");
const { MerkleTree } = require("merkletreejs");
const keccak256 = require("keccak256");
const fs = require("fs");

// REAL BENEFICIARIES — UPDATE THESE BEFORE FINAL DEPLOY
const charities = [
  { name: "St. Jude",        address: "0x5555555555555555555555555555555555555555", amount: hre.ethers.parseEther("1.5") },
  { name: "MSF",             address: "0x6666666666666666666666666666666666666666", amount: hre.ethers.parseEther("1.5") },
  { name: "Veterans",        address: "0x7777777777777777777777777777777777777777", amount: hre.ethers.parseEther("0.5") }
];

async function main() {
  console.log("Generating Merkle Tree for SwarmGate v1.0...");

  const leaves = charities.map((c, i) =>
    hre.ethers.solidityPackedKeccak256(["uint256", "address", "uint256"], [i, c.address, c.amount])
  );

  const tree = new MerkleTree(leaves, keccak256, { sortPairs: true });
  const root = tree.getHexRoot();
  console.log("\nMERKLE ROOT → DEPLOY THIS:");
  console.log(root);

  const proofs = charities.map((c, i) => ({
    name: c.name,
    address: c.address,
    amount: c.amount.toString(),
    index: i,
    proof: tree.getHexProof(leaves[i])
  }));

  const output = { root, proofs };
  fs.writeFileSync("merkle-data.json", JSON.stringify(output, null, 2));
  console.log("\nProofs saved → merkle-data.json");
}

main().catch(err => { console.error(err); process.exit(1); });
