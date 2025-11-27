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

  it("93/7 split is mathematically perfect — delta-based verification", async function () {
    const amount = ethers.parseEther("100");

    // Record balances BEFORE the split
    const opsBefore = await ethers.provider.getBalance(ops.address);
    const distBefore = await ethers.provider.getBalance(await distributor.getAddress());

    // Execute the split
    await owner.sendTransaction({ to: await splitter.getAddress(), value: amount });

    // Record balances AFTER the split
    const opsAfter = await ethers.provider.getBalance(ops.address);
    const distAfter = await ethers.provider.getBalance(await distributor.getAddress());

    // Verify the exact delta — works regardless of starting balance
    expect(opsAfter - opsBefore).to.equal(ethers.parseEther("93"));
    expect(distAfter - distBefore).to.equal(ethers.parseEther("7"));
  });
});
