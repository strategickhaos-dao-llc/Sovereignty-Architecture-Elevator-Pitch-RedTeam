// SwarmGate v1.0 - Smart Contract Tests
// Tests for CharitySplitter and MerkleDistributor
// Author: Strategickhaos DAO LLC / ValorYield Engine

const { expect } = require("chai");
const { ethers } = require("hardhat");
const { MerkleTree } = require("merkletreejs");
const keccak256 = require("keccak256");

describe("SwarmGate v1.0 Smart Contracts", function () {
  let charitySplitter;
  let merkleDistributor;
  let owner;
  let charityPool;
  let treasury;
  let user1;
  let user2;

  beforeEach(async function () {
    [owner, charityPool, treasury, user1, user2] = await ethers.getSigners();
  });

  describe("CharitySplitter", function () {
    beforeEach(async function () {
      const CharitySplitter = await ethers.getContractFactory("CharitySplitter");
      charitySplitter = await CharitySplitter.deploy(
        charityPool.address,
        treasury.address
      );
      await charitySplitter.waitForDeployment();
    });

    it("Should set the correct charity and treasury addresses", async function () {
      expect(await charitySplitter.charityPool()).to.equal(charityPool.address);
      expect(await charitySplitter.treasury()).to.equal(treasury.address);
    });

    it("Should have correct constants for 7% split", async function () {
      expect(await charitySplitter.CHARITY_BPS()).to.equal(700);
      expect(await charitySplitter.BPS_DENOMINATOR()).to.equal(10000);
    });

    it("Should split incoming ETH correctly (7% charity, 93% treasury)", async function () {
      const sendAmount = ethers.parseEther("1.0");
      const expectedCharity = (sendAmount * BigInt(700)) / BigInt(10000);
      const expectedTreasury = sendAmount - expectedCharity;

      const charityBalanceBefore = await ethers.provider.getBalance(charityPool.address);
      const treasuryBalanceBefore = await ethers.provider.getBalance(treasury.address);

      // Send ETH to the splitter
      await owner.sendTransaction({
        to: await charitySplitter.getAddress(),
        value: sendAmount,
      });

      const charityBalanceAfter = await ethers.provider.getBalance(charityPool.address);
      const treasuryBalanceAfter = await ethers.provider.getBalance(treasury.address);

      expect(charityBalanceAfter - charityBalanceBefore).to.equal(expectedCharity);
      expect(treasuryBalanceAfter - treasuryBalanceBefore).to.equal(expectedTreasury);
    });

    it("Should track total received correctly", async function () {
      const amount1 = ethers.parseEther("1.0");
      const amount2 = ethers.parseEther("2.0");

      await owner.sendTransaction({
        to: await charitySplitter.getAddress(),
        value: amount1,
      });

      await user1.sendTransaction({
        to: await charitySplitter.getAddress(),
        value: amount2,
      });

      const [totalReceived, totalToCharity, totalToTreasury] = await charitySplitter.getStats();
      expect(totalReceived).to.equal(amount1 + amount2);
    });

    it("Should only allow owner to update charity pool", async function () {
      await expect(
        charitySplitter.connect(user1).setCharityPool(user2.address)
      ).to.be.revertedWithCustomError(charitySplitter, "OwnableUnauthorizedAccount");
    });

    it("Should only allow owner to update treasury", async function () {
      await expect(
        charitySplitter.connect(user1).setTreasury(user2.address)
      ).to.be.revertedWithCustomError(charitySplitter, "OwnableUnauthorizedAccount");
    });
  });

  describe("MerkleDistributor", function () {
    let merkleTree;
    let leaves;
    let claims;

    beforeEach(async function () {
      const MerkleDistributor = await ethers.getContractFactory("MerkleDistributor");
      merkleDistributor = await MerkleDistributor.deploy();
      await merkleDistributor.waitForDeployment();

      // Set up merkle tree for claims
      claims = [
        { address: user1.address, amount: ethers.parseEther("0.5") },
        { address: user2.address, amount: ethers.parseEther("0.3") },
      ];

      leaves = claims.map((claim) =>
        ethers.keccak256(
          ethers.solidityPacked(
            ["bytes32"],
            [ethers.keccak256(ethers.AbiCoder.defaultAbiCoder().encode(
              ["address", "uint256"],
              [claim.address, claim.amount]
            ))]
          )
        )
      );

      merkleTree = new MerkleTree(leaves, keccak256, { sortPairs: true });
    });

    it("Should initialize with round 1", async function () {
      expect(await merkleDistributor.currentRound()).to.equal(1);
    });

    it("Should allow owner to set merkle root", async function () {
      const root = merkleTree.getHexRoot();
      await merkleDistributor.setMerkleRoot(root);
      expect(await merkleDistributor.merkleRoot()).to.equal(root);
    });

    it("Should only allow owner to set merkle root", async function () {
      const root = merkleTree.getHexRoot();
      await expect(
        merkleDistributor.connect(user1).setMerkleRoot(root)
      ).to.be.revertedWithCustomError(merkleDistributor, "OwnableUnauthorizedAccount");
    });

    it("Should advance round correctly", async function () {
      const root = merkleTree.getHexRoot();
      await merkleDistributor.advanceRound(root);
      expect(await merkleDistributor.currentRound()).to.equal(2);
    });

    it("Should receive ETH deposits", async function () {
      const amount = ethers.parseEther("1.0");
      await owner.sendTransaction({
        to: await merkleDistributor.getAddress(),
        value: amount,
      });
      expect(await merkleDistributor.getBalance()).to.equal(amount);
    });

    it("Should return correct stats", async function () {
      const [round, totalDist, roundDist, balance] = await merkleDistributor.getStats();
      expect(round).to.equal(1);
      expect(totalDist).to.equal(0);
      expect(roundDist).to.equal(0);
    });
  });
});
