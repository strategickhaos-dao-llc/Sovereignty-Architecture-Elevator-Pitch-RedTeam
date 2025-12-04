const { buildModule } = require("@nomicfoundation/hardhat-ignition/modules");

/**
 * Hardhat Ignition module for deploying the Charity Splitter system
 * 
 * This deploys:
 * 1. MerkleDistributor - for distributing 7% to named charities
 * 2. CharitySplitter - the main payment splitter (93% ops / 7% charity)
 */
module.exports = buildModule("CharitySplitterModule", (m) => {
  // Get deployment parameters
  const opsMultisig = m.getParameter("opsMultisig");
  const merkleRoot = m.getParameter("merkleRoot");
  const charityCount = m.getParameter("charityCount", 7); // Default: 7 charities

  // Deploy MerkleDistributor first
  const merkleDistributor = m.contract("MerkleDistributor", [merkleRoot, charityCount]);

  // Deploy CharitySplitter with ops multisig and distributor addresses
  const charitySplitter = m.contract("CharitySplitter", [opsMultisig, merkleDistributor]);

  return { merkleDistributor, charitySplitter };
});
