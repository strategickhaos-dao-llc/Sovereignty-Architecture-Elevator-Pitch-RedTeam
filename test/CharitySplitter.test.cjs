/**
 * @title Strategickhaos 7% Charity Splitter Tests
 * @notice Validates the irrevocable 93%/7% split and Merkle claim functionality
 * @dev Run with: npx hardhat test
 */

const { expect } = require("chai");
const { ethers } = require("hardhat");
const { MerkleTree } = require("merkletreejs");
const keccak256 = require("keccak256");

describe("Strategickhaos 7% Charity Engine", function () {
  let CharitySplitter, MerkleDistributor;
  let splitter, distributor;
  let owner, opsWallet, charity1, charity2, attacker;
  let merkleTree, root, leaves;

  const CHARITY_AMOUNT = ethers.parseEther("1.0"); // 1 ETH claim

  /**
   * Generate a leaf node for the Merkle tree
   * Uses keccak256(abi.encode()) to match the contract
   */
  function generateLeaf(index, address, amount) {
    const abiCoder = ethers.AbiCoder.defaultAbiCoder();
    const encoded = abiCoder.encode(
      ["uint256", "address", "uint256"],
      [index, address, amount]
    );
    return Buffer.from(ethers.keccak256(encoded).slice(2), "hex");
  }

  beforeEach(async function () {
    [owner, opsWallet, charity1, charity2, attacker] = await ethers.getSigners();

    // --- Setup Merkle Tree with two charities ---
    leaves = [
      generateLeaf(0, charity1.address, CHARITY_AMOUNT),
      generateLeaf(1, charity2.address, ethers.parseEther("0.5"))
    ];
    
    merkleTree = new MerkleTree(leaves, keccak256, { sortPairs: true });
    root = merkleTree.getHexRoot();

    // --- Deploy MerkleDistributor ---
    MerkleDistributor = await ethers.getContractFactory("MerkleDistributor");
    distributor = await MerkleDistributor.deploy(root);
    await distributor.waitForDeployment();

    // --- Deploy CharitySplitter ---
    CharitySplitter = await ethers.getContractFactory("CharitySplitter");
    splitter = await CharitySplitter.deploy(opsWallet.address, await distributor.getAddress());
    await splitter.waitForDeployment();
  });

  describe("CharitySplitter", function () {
    it("Should split incoming funds 93% / 7% irrevocably", async function () {
      const inputAmount = ethers.parseEther("100");
      
      // Track balances before
      const opsBefore = await ethers.provider.getBalance(opsWallet.address);
      const distBefore = await ethers.provider.getBalance(await distributor.getAddress());

      // Send 100 ETH to Splitter
      await owner.sendTransaction({
        to: await splitter.getAddress(),
        value: inputAmount
      });

      // Track balances after
      const opsAfter = await ethers.provider.getBalance(opsWallet.address);
      const distAfter = await ethers.provider.getBalance(await distributor.getAddress());

      // Verify 93% went to Ops (93 ETH)
      expect(opsAfter - opsBefore).to.equal(ethers.parseEther("93"));
      
      // Verify 7% went to Distributor (7 ETH)
      expect(distAfter - distBefore).to.equal(ethers.parseEther("7"));
    });

    it("Should emit FundsSplit event with correct amounts", async function () {
      const inputAmount = ethers.parseEther("10");
      
      await expect(
        owner.sendTransaction({
          to: await splitter.getAddress(),
          value: inputAmount
        })
      )
      .to.emit(splitter, "FundsSplit")
      .withArgs(
        owner.address,
        inputAmount,
        ethers.parseEther("9.3"),  // 93% ops
        ethers.parseEther("0.7")   // 7% charity
      );
    });

    it("Should correctly calculate split amounts", async function () {
      const amount = ethers.parseEther("1000");
      const [opsAmount, charityAmount] = await splitter.calculateSplit(amount);
      
      expect(opsAmount).to.equal(ethers.parseEther("930"));    // 93%
      expect(charityAmount).to.equal(ethers.parseEther("70")); // 7%
    });

    it("Should have immutable wallet addresses", async function () {
      expect(await splitter.opsWallet()).to.equal(opsWallet.address);
      expect(await splitter.charityDistributor()).to.equal(await distributor.getAddress());
    });

    it("Should have correct charity basis points", async function () {
      expect(await splitter.CHARITY_BPS()).to.equal(700n);
      expect(await splitter.BPS_DENOMINATOR()).to.equal(10000n);
    });

    it("Should reject deployment with zero address for ops wallet", async function () {
      const CharitySplitterFactory = await ethers.getContractFactory("CharitySplitter");
      await expect(
        CharitySplitterFactory.deploy(ethers.ZeroAddress, await distributor.getAddress())
      ).to.be.revertedWithCustomError(CharitySplitterFactory, "ZeroAddress");
    });

    it("Should reject deployment with zero address for charity distributor", async function () {
      const CharitySplitterFactory = await ethers.getContractFactory("CharitySplitter");
      await expect(
        CharitySplitterFactory.deploy(opsWallet.address, ethers.ZeroAddress)
      ).to.be.revertedWithCustomError(CharitySplitterFactory, "ZeroAddress");
    });
  });

  describe("MerkleDistributor", function () {
    beforeEach(async function () {
      // Fund the distributor (simulating a split happened)
      await owner.sendTransaction({
        to: await distributor.getAddress(),
        value: ethers.parseEther("2") // Enough for both claims
      });
    });

    it("Should allow valid charity to claim via Merkle Proof", async function () {
      const leaf = leaves[0];
      const proof = merkleTree.getHexProof(leaf);
      const balanceBefore = await ethers.provider.getBalance(charity1.address);

      // Execute Claim
      await expect(
        distributor.connect(charity1).claim(0, charity1.address, CHARITY_AMOUNT, proof)
      )
      .to.emit(distributor, "Claimed")
      .withArgs(0, charity1.address, CHARITY_AMOUNT);

      // Verify balance increased
      const balanceAfter = await ethers.provider.getBalance(charity1.address);
      // Account for gas costs - just verify it increased significantly
      expect(balanceAfter).to.be.gt(balanceBefore);
    });

    it("Should mark claim as used after claiming", async function () {
      const leaf = leaves[0];
      const proof = merkleTree.getHexProof(leaf);

      expect(await distributor.isClaimed(0)).to.be.false;
      
      await distributor.connect(charity1).claim(0, charity1.address, CHARITY_AMOUNT, proof);
      
      expect(await distributor.isClaimed(0)).to.be.true;
    });

    it("Should reject double claims", async function () {
      const leaf = leaves[0];
      const proof = merkleTree.getHexProof(leaf);

      // First claim succeeds
      await distributor.connect(charity1).claim(0, charity1.address, CHARITY_AMOUNT, proof);

      // Second claim fails
      await expect(
        distributor.connect(charity1).claim(0, charity1.address, CHARITY_AMOUNT, proof)
      ).to.be.revertedWithCustomError(distributor, "AlreadyClaimed");
    });

    it("Should reject claims with invalid proof", async function () {
      const fakeProof = [
        "0x" + "1".repeat(64),
        "0x" + "2".repeat(64)
      ];

      await expect(
        distributor.connect(attacker).claim(0, attacker.address, CHARITY_AMOUNT, fakeProof)
      ).to.be.revertedWithCustomError(distributor, "InvalidProof");
    });

    it("Should reject claims with wrong amount", async function () {
      const leaf = leaves[0];
      const proof = merkleTree.getHexProof(leaf);
      const wrongAmount = ethers.parseEther("999"); // Not what's in the tree

      await expect(
        distributor.connect(charity1).claim(0, charity1.address, wrongAmount, proof)
      ).to.be.revertedWithCustomError(distributor, "InvalidProof");
    });

    it("Should reject claims with wrong address", async function () {
      const leaf = leaves[0];
      const proof = merkleTree.getHexProof(leaf);

      // Try to claim with attacker address using charity1's proof
      await expect(
        distributor.connect(attacker).claim(0, attacker.address, CHARITY_AMOUNT, proof)
      ).to.be.revertedWithCustomError(distributor, "InvalidProof");
    });

    it("Should allow owner to update merkle root", async function () {
      const newRoot = "0x" + "a".repeat(64);
      
      await expect(distributor.connect(owner).updateMerkleRoot(newRoot))
        .to.emit(distributor, "MerkleRootUpdated")
        .withArgs(root, newRoot);

      expect(await distributor.merkleRoot()).to.equal(newRoot);
    });

    it("Should reject non-owner from updating merkle root", async function () {
      const newRoot = "0x" + "a".repeat(64);
      
      await expect(
        distributor.connect(attacker).updateMerkleRoot(newRoot)
      ).to.be.revertedWithCustomError(distributor, "OwnableUnauthorizedAccount");
    });

    it("Should reject zero merkle root", async function () {
      await expect(
        distributor.connect(owner).updateMerkleRoot(ethers.ZeroHash)
      ).to.be.revertedWithCustomError(distributor, "ZeroRoot");
    });

    it("Should return correct balance", async function () {
      const balance = await distributor.getBalance();
      expect(balance).to.equal(ethers.parseEther("2"));
    });

    it("Should reject deployment with zero merkle root", async function () {
      const MerkleDistributorFactory = await ethers.getContractFactory("MerkleDistributor");
      await expect(
        MerkleDistributorFactory.deploy(ethers.ZeroHash)
      ).to.be.revertedWithCustomError(MerkleDistributorFactory, "ZeroRoot");
    });
  });

  describe("Integration: Full Split and Claim Flow", function () {
    it("Should complete full cycle: deposit → split → claim", async function () {
      // Step 1: Send 100 ETH to splitter
      const depositAmount = ethers.parseEther("100");
      await owner.sendTransaction({
        to: await splitter.getAddress(),
        value: depositAmount
      });

      // Step 2: Verify distributor received 7 ETH
      const distributorBalance = await distributor.getBalance();
      expect(distributorBalance).to.equal(ethers.parseEther("7"));

      // Step 3: Charity claims their allocation
      const leaf = leaves[0];
      const proof = merkleTree.getHexProof(leaf);
      
      const balanceBefore = await ethers.provider.getBalance(charity1.address);
      
      const tx = await distributor.connect(charity1).claim(0, charity1.address, CHARITY_AMOUNT, proof);
      const receipt = await tx.wait();
      const gasCost = receipt.gasUsed * receipt.gasPrice;

      const balanceAfter = await ethers.provider.getBalance(charity1.address);
      
      // Charity should have received 1 ETH minus gas
      expect(balanceAfter).to.equal(balanceBefore + CHARITY_AMOUNT - gasCost);

      // Step 4: Verify distributor balance decreased
      const newDistributorBalance = await distributor.getBalance();
      expect(newDistributorBalance).to.equal(ethers.parseEther("6")); // 7 - 1 = 6 ETH remaining
    });
  });
});
