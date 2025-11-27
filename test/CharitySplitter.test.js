const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SwarmGate v1.0 Engine", function () {
  let splitter, distributor, owner, ops, charity;

  beforeEach(async function () {
    [owner, ops, charity] = await ethers.getSigners();

    const Distributor = await ethers.getContractFactory("MerkleDistributor");
    distributor = await Distributor.deploy("0x" + "0".repeat(64));
    await distributor.waitForDeployment();

    const Splitter = await ethers.getContractFactory("CharitySplitter");
    splitter = await Splitter.deploy(ops.address, await distributor.getAddress());
    await splitter.waitForDeployment();
  });

  it("93/7 split is mathematically perfect", async function () {
    const amount = ethers.parseEther("100");
    
    // Capture initial balances
    const opsBalBefore = await ethers.provider.getBalance(ops.address);
    const distBalBefore = await ethers.provider.getBalance(await distributor.getAddress());
    
    await owner.sendTransaction({ to: await splitter.getAddress(), value: amount });

    const opsBalAfter = await ethers.provider.getBalance(ops.address);
    const distBalAfter = await ethers.provider.getBalance(await distributor.getAddress());

    // Verify the split amounts (93 ETH to ops, 7 ETH to charity)
    expect(opsBalAfter - opsBalBefore).to.equal(ethers.parseEther("93"));
    expect(distBalAfter - distBalBefore).to.equal(ethers.parseEther("7"));
  });
});
