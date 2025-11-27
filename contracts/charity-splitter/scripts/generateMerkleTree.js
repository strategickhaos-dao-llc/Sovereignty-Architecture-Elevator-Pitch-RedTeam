const { StandardMerkleTree } = require("@openzeppelin/merkle-tree");
const fs = require("fs");

/**
 * Script to generate Merkle tree for charity distribution
 * 
 * Named Charities (7% allocation split equally):
 * 1. St. Jude Children's Research Hospital
 * 2. Doctors Without Borders
 * 3. Electronic Frontier Foundation
 * 4. Direct Relief
 * 5. charity: water
 * 6. World Wildlife Fund
 * 7. Feeding America
 */

// Example charity addresses (replace with actual verified addresses before mainnet deployment)
const charities = [
  [0, "0x1111111111111111111111111111111111111111"], // St. Jude (placeholder)
  [1, "0x2222222222222222222222222222222222222222"], // Doctors Without Borders (placeholder)
  [2, "0x3333333333333333333333333333333333333333"], // Electronic Frontier Foundation (placeholder)
  [3, "0x4444444444444444444444444444444444444444"], // Direct Relief (placeholder)
  [4, "0x5555555555555555555555555555555555555555"], // charity: water (placeholder)
  [5, "0x6666666666666666666666666666666666666666"], // World Wildlife Fund (placeholder)
  [6, "0x7777777777777777777777777777777777777777"], // Feeding America (placeholder)
];

// Build Merkle tree
const tree = StandardMerkleTree.of(charities, ["uint256", "address"]);

console.log("=== Charity Merkle Tree Generated ===");
console.log("");
console.log("Merkle Root:", tree.root);
console.log("Charity Count:", charities.length);
console.log("");
console.log("Charities:");
charities.forEach(([index, address], i) => {
  const names = [
    "St. Jude Children's Research Hospital",
    "Doctors Without Borders",
    "Electronic Frontier Foundation",
    "Direct Relief",
    "charity: water",
    "World Wildlife Fund",
    "Feeding America"
  ];
  console.log(`  ${index}: ${names[i]} - ${address}`);
});
console.log("");

// Generate proofs for each charity
console.log("Proofs:");
charities.forEach(([index, address]) => {
  const proof = tree.getProof([index, address]);
  console.log(`  Charity ${index}: ${JSON.stringify(proof)}`);
});

// Save tree to file
const treeData = {
  root: tree.root,
  charityCount: charities.length,
  charities: charities.map(([index, address], i) => {
    const names = [
      "St. Jude Children's Research Hospital",
      "Doctors Without Borders",
      "Electronic Frontier Foundation",
      "Direct Relief",
      "charity: water",
      "World Wildlife Fund",
      "Feeding America"
    ];
    return {
      index,
      name: names[i],
      address,
      proof: tree.getProof([index, address])
    };
  }),
  tree: tree.dump()
};

// Ensure output directory exists
if (!fs.existsSync("./merkle")) {
  fs.mkdirSync("./merkle", { recursive: true });
}

fs.writeFileSync("./merkle/charity-tree.json", JSON.stringify(treeData, null, 2));
console.log("");
console.log("Tree saved to: ./merkle/charity-tree.json");
console.log("");
console.log("=== Deployment Parameters ===");
console.log(`merkleRoot: "${tree.root}"`);
console.log(`charityCount: ${charities.length}`);
