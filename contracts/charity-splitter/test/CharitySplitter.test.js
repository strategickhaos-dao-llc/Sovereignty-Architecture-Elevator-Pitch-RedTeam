const { expect } = require("chai");
const { ethers } = require("hardhat");
const { loadFixture } = require("@nomicfoundation/hardhat-toolbox/network-helpers");
const { StandardMerkleTree } = require("@openzeppelin/merkle-tree");

describe("CharitySplitter", function () {
  // Fixture to deploy contracts
  async function deployCharitySplitterFixture() {
    const [owner, ops, charity1, charity2, charity3, user] = await ethers.getSigners();

    // Create charity list for Merkle tree
    const charities = [
      [0, charity1.address],
      [1, charity2.address],
      [2, charity3.address],
    ];

    // Build Merkle tree
    const tree = StandardMerkleTree.of(charities, ["uint256", "address"]);
    const merkleRoot = tree.root;

    // Deploy MerkleDistributor
    const MerkleDistributor = await ethers.getContractFactory("MerkleDistributor");
    const distributor = await MerkleDistributor.deploy(merkleRoot, 3);
    await distributor.waitForDeployment();

    // Deploy CharitySplitter
    const CharitySplitter = await ethers.getContractFactory("CharitySplitter");
    const splitter = await CharitySplitter.deploy(ops.address, await distributor.getAddress());
    await splitter.waitForDeployment();

    return { splitter, distributor, tree, owner, ops, charity1, charity2, charity3, user };
  }

  describe("Deployment", function () {
    it("Should set the correct charity percentage (7%)", async function () {
      const { splitter } = await loadFixture(deployCharitySplitterFixture);
      expect(await splitter.getCharityPercentage()).to.equal(7n);
    });

    it("Should set immutable ops address", async function () {
      const { splitter, ops } = await loadFixture(deployCharitySplitterFixture);
      expect(await splitter.opsMultisig()).to.equal(ops.address);
    });

    it("Should set immutable charity distributor address", async function () {
      const { splitter, distributor } = await loadFixture(deployCharitySplitterFixture);
      expect(await splitter.charityDistributor()).to.equal(await distributor.getAddress());
    });

    it("Should reject zero addresses", async function () {
      const [owner, ops] = await ethers.getSigners();
      const CharitySplitter = await ethers.getContractFactory("CharitySplitter");
      
      await expect(
        CharitySplitter.deploy(ethers.ZeroAddress, ops.address)
      ).to.be.revertedWith("Invalid ops address");
      
      await expect(
        CharitySplitter.deploy(ops.address, ethers.ZeroAddress)
      ).to.be.revertedWith("Invalid charity address");
    });

    it("Should reject same address for ops and charity", async function () {
      const [owner, ops] = await ethers.getSigners();
      const CharitySplitter = await ethers.getContractFactory("CharitySplitter");
      
      await expect(
        CharitySplitter.deploy(ops.address, ops.address)
      ).to.be.revertedWith("Addresses must be different");
    });
  });

  describe("Distribution", function () {
    it("Should split incoming ETH: 93% to ops, 7% to charity", async function () {
      const { splitter, distributor, ops, user } = await loadFixture(deployCharitySplitterFixture);
      
      const amount = ethers.parseEther("1.0");
      const expectedCharity = amount * 700n / 10000n; // 7%
      const expectedOps = amount - expectedCharity; // 93%
      
      const opsBalanceBefore = await ethers.provider.getBalance(ops.address);
      const distributorAddress = await distributor.getAddress();
      const distributorBalanceBefore = await ethers.provider.getBalance(distributorAddress);
      
      // Send ETH to splitter
      await user.sendTransaction({
        to: await splitter.getAddress(),
        value: amount
      });
      
      const opsBalanceAfter = await ethers.provider.getBalance(ops.address);
      const distributorBalanceAfter = await ethers.provider.getBalance(distributorAddress);
      
      expect(opsBalanceAfter - opsBalanceBefore).to.equal(expectedOps);
      expect(distributorBalanceAfter - distributorBalanceBefore).to.equal(expectedCharity);
    });

    it("Should track total received correctly", async function () {
      const { splitter, user } = await loadFixture(deployCharitySplitterFixture);
      
      const amount1 = ethers.parseEther("1.0");
      const amount2 = ethers.parseEther("2.5");
      
      await user.sendTransaction({
        to: await splitter.getAddress(),
        value: amount1
      });
      
      await user.sendTransaction({
        to: await splitter.getAddress(),
        value: amount2
      });
      
      expect(await splitter.totalReceived()).to.equal(amount1 + amount2);
    });

    it("Should track totalToCharity correctly (7% forever counter)", async function () {
      const { splitter, user } = await loadFixture(deployCharitySplitterFixture);
      
      const amount = ethers.parseEther("10.0");
      const expectedCharity = amount * 700n / 10000n;
      
      await user.sendTransaction({
        to: await splitter.getAddress(),
        value: amount
      });
      
      expect(await splitter.totalToCharity()).to.equal(expectedCharity);
    });

    it("Should emit Distribution event", async function () {
      const { splitter, user } = await loadFixture(deployCharitySplitterFixture);
      
      const amount = ethers.parseEther("1.0");
      const expectedCharity = amount * 700n / 10000n;
      const expectedOps = amount - expectedCharity;
      
      await expect(
        user.sendTransaction({
          to: await splitter.getAddress(),
          value: amount
        })
      ).to.emit(splitter, "Distribution")
        .withArgs(1n, amount, expectedOps, expectedCharity, (timestamp) => timestamp > 0);
    });

    it("Should increment distribution count", async function () {
      const { splitter, user } = await loadFixture(deployCharitySplitterFixture);
      
      expect(await splitter.distributionCount()).to.equal(0n);
      
      await user.sendTransaction({
        to: await splitter.getAddress(),
        value: ethers.parseEther("1.0")
      });
      
      expect(await splitter.distributionCount()).to.equal(1n);
      
      await user.sendTransaction({
        to: await splitter.getAddress(),
        value: ethers.parseEther("0.5")
      });
      
      expect(await splitter.distributionCount()).to.equal(2n);
    });
  });

  describe("Statistics", function () {
    it("Should return correct stats via getStats()", async function () {
      const { splitter, user } = await loadFixture(deployCharitySplitterFixture);
      
      const amount = ethers.parseEther("5.0");
      const expectedCharity = amount * 700n / 10000n;
      const expectedOps = amount - expectedCharity;
      
      await user.sendTransaction({
        to: await splitter.getAddress(),
        value: amount
      });
      
      const [received, toOps, toCharity, distributions] = await splitter.getStats();
      
      expect(received).to.equal(amount);
      expect(toOps).to.equal(expectedOps);
      expect(toCharity).to.equal(expectedCharity);
      expect(distributions).to.equal(1n);
    });
  });
});

describe("MerkleDistributor", function () {
  async function deployMerkleDistributorFixture() {
    const [owner, charity1, charity2, charity3, user] = await ethers.getSigners();

    // Create charity list for Merkle tree
    const charities = [
      [0, charity1.address],
      [1, charity2.address],
      [2, charity3.address],
    ];

    // Build Merkle tree
    const tree = StandardMerkleTree.of(charities, ["uint256", "address"]);
    const merkleRoot = tree.root;

    // Deploy MerkleDistributor
    const MerkleDistributor = await ethers.getContractFactory("MerkleDistributor");
    const distributor = await MerkleDistributor.deploy(merkleRoot, 3);
    await distributor.waitForDeployment();

    return { distributor, tree, owner, charity1, charity2, charity3, user };
  }

  describe("Deployment", function () {
    it("Should set the correct merkle root", async function () {
      const { distributor, tree } = await loadFixture(deployMerkleDistributorFixture);
      expect(await distributor.merkleRoot()).to.equal(tree.root);
    });

    it("Should set the correct charity count", async function () {
      const { distributor } = await loadFixture(deployMerkleDistributorFixture);
      expect(await distributor.charityCount()).to.equal(3n);
    });

    it("Should reject zero merkle root", async function () {
      const MerkleDistributor = await ethers.getContractFactory("MerkleDistributor");
      await expect(
        MerkleDistributor.deploy(ethers.ZeroHash, 3)
      ).to.be.revertedWith("Invalid merkle root");
    });

    it("Should reject zero charity count", async function () {
      const MerkleDistributor = await ethers.getContractFactory("MerkleDistributor");
      await expect(
        MerkleDistributor.deploy(ethers.randomBytes(32), 0)
      ).to.be.revertedWith("Must have at least one charity");
    });
  });

  describe("Receiving Funds", function () {
    it("Should receive and track funds", async function () {
      const { distributor, user } = await loadFixture(deployMerkleDistributorFixture);
      
      const amount = ethers.parseEther("0.7"); // 7% of 10 ETH
      
      await user.sendTransaction({
        to: await distributor.getAddress(),
        value: amount
      });
      
      expect(await distributor.totalReceived()).to.equal(amount);
      expect(await distributor.currentEpoch()).to.equal(1n);
    });

    it("Should emit FundsReceived event", async function () {
      const { distributor, user } = await loadFixture(deployMerkleDistributorFixture);
      
      const amount = ethers.parseEther("1.0");
      
      await expect(
        user.sendTransaction({
          to: await distributor.getAddress(),
          value: amount
        })
      ).to.emit(distributor, "FundsReceived");
    });
  });

  describe("Charity Claims", function () {
    it("Should allow verified charity to claim", async function () {
      const { distributor, tree, charity1, user } = await loadFixture(deployMerkleDistributorFixture);
      
      // Send funds to distributor
      const amount = ethers.parseEther("0.9"); // Will be split 3 ways
      await user.sendTransaction({
        to: await distributor.getAddress(),
        value: amount
      });
      
      // Get proof for charity1
      const proof = tree.getProof([0, charity1.address]);
      
      const balanceBefore = await ethers.provider.getBalance(charity1.address);
      
      // Charity1 claims
      await distributor.claim(0, charity1.address, proof);
      
      const balanceAfter = await ethers.provider.getBalance(charity1.address);
      const expectedShare = amount / 3n;
      
      expect(balanceAfter - balanceBefore).to.equal(expectedShare);
    });

    it("Should verify charity with merkle proof", async function () {
      const { distributor, tree, charity1, charity2 } = await loadFixture(deployMerkleDistributorFixture);
      
      const proof1 = tree.getProof([0, charity1.address]);
      const proof2 = tree.getProof([1, charity2.address]);
      
      expect(await distributor.verifyCharity(0, charity1.address, proof1)).to.be.true;
      expect(await distributor.verifyCharity(1, charity2.address, proof2)).to.be.true;
      
      // Invalid proof should fail
      expect(await distributor.verifyCharity(0, charity2.address, proof1)).to.be.false;
    });

    it("Should reject invalid merkle proof", async function () {
      const { distributor, tree, charity1, charity2, user } = await loadFixture(deployMerkleDistributorFixture);
      
      // Send funds
      await user.sendTransaction({
        to: await distributor.getAddress(),
        value: ethers.parseEther("1.0")
      });
      
      // Try to claim with wrong proof
      const wrongProof = tree.getProof([1, charity2.address]);
      
      await expect(
        distributor.claim(0, charity1.address, wrongProof)
      ).to.be.revertedWith("Invalid proof");
    });

    it("Should prevent double claiming in same epoch", async function () {
      const { distributor, tree, charity1, user } = await loadFixture(deployMerkleDistributorFixture);
      
      // Send funds
      await user.sendTransaction({
        to: await distributor.getAddress(),
        value: ethers.parseEther("1.0")
      });
      
      const proof = tree.getProof([0, charity1.address]);
      
      // First claim succeeds
      await distributor.claim(0, charity1.address, proof);
      
      // Second claim fails
      await expect(
        distributor.claim(0, charity1.address, proof)
      ).to.be.revertedWith("Already claimed in epoch");
    });

    it("Should give remainder dust to last claimer", async function () {
      const { distributor, tree, charity1, charity2, charity3, user } = await loadFixture(deployMerkleDistributorFixture);
      
      // Send amount that doesn't divide evenly by 3
      // 10 wei = 3 wei * 3 + 1 wei remainder
      const amount = 10n;
      await user.sendTransaction({
        to: await distributor.getAddress(),
        value: amount
      });
      
      const proof1 = tree.getProof([0, charity1.address]);
      const proof2 = tree.getProof([1, charity2.address]);
      const proof3 = tree.getProof([2, charity3.address]);
      
      // Get balances before
      const charity1Before = await ethers.provider.getBalance(charity1.address);
      const charity2Before = await ethers.provider.getBalance(charity2.address);
      const charity3Before = await ethers.provider.getBalance(charity3.address);
      
      // All three claim
      await distributor.claim(0, charity1.address, proof1);
      await distributor.claim(1, charity2.address, proof2);
      await distributor.claim(2, charity3.address, proof3);
      
      // Get balances after
      const charity1After = await ethers.provider.getBalance(charity1.address);
      const charity2After = await ethers.provider.getBalance(charity2.address);
      const charity3After = await ethers.provider.getBalance(charity3.address);
      
      // First two get base share (3 wei), last one gets base + remainder (3 + 1 = 4 wei)
      expect(charity1After - charity1Before).to.equal(3n);
      expect(charity2After - charity2Before).to.equal(3n);
      expect(charity3After - charity3Before).to.equal(4n); // Gets the 1 wei remainder
      
      // Verify total distributed equals total received (no dust locked)
      const distributorBalance = await ethers.provider.getBalance(await distributor.getAddress());
      expect(distributorBalance).to.equal(0n);
    });
  });

  describe("Statistics", function () {
    it("Should return correct stats via getStats()", async function () {
      const { distributor, tree, charity1, user } = await loadFixture(deployMerkleDistributorFixture);
      
      const amount = ethers.parseEther("0.9");
      
      await user.sendTransaction({
        to: await distributor.getAddress(),
        value: amount
      });
      
      const proof = tree.getProof([0, charity1.address]);
      await distributor.claim(0, charity1.address, proof);
      
      const [received, claimed, pending, epoch] = await distributor.getStats();
      
      expect(received).to.equal(amount);
      expect(claimed).to.equal(amount / 3n);
      expect(epoch).to.equal(1n);
    });
  });
});

describe("Integration: CharitySplitter + MerkleDistributor", function () {
  async function deployFullSystemFixture() {
    const [owner, ops, charity1, charity2, charity3, user] = await ethers.getSigners();

    // Create charity list for Merkle tree
    const charities = [
      [0, charity1.address],
      [1, charity2.address],
      [2, charity3.address],
    ];

    // Build Merkle tree
    const tree = StandardMerkleTree.of(charities, ["uint256", "address"]);
    const merkleRoot = tree.root;

    // Deploy MerkleDistributor
    const MerkleDistributor = await ethers.getContractFactory("MerkleDistributor");
    const distributor = await MerkleDistributor.deploy(merkleRoot, 3);
    await distributor.waitForDeployment();

    // Deploy CharitySplitter
    const CharitySplitter = await ethers.getContractFactory("CharitySplitter");
    const splitter = await CharitySplitter.deploy(ops.address, await distributor.getAddress());
    await splitter.waitForDeployment();

    return { splitter, distributor, tree, owner, ops, charity1, charity2, charity3, user };
  }

  it("Should complete full flow: receive -> split -> claim", async function () {
    const { splitter, distributor, tree, ops, charity1, charity2, charity3, user } = await loadFixture(deployFullSystemFixture);
    
    // User sends 10 ETH to splitter
    const amount = ethers.parseEther("10.0");
    await user.sendTransaction({
      to: await splitter.getAddress(),
      value: amount
    });
    
    // Verify splitter stats
    const expectedCharity = amount * 700n / 10000n; // 0.7 ETH
    const expectedOps = amount - expectedCharity; // 9.3 ETH
    
    expect(await splitter.totalToCharity()).to.equal(expectedCharity);
    expect(await splitter.totalToOps()).to.equal(expectedOps);
    
    // Verify distributor received the 7%
    expect(await distributor.totalReceived()).to.equal(expectedCharity);
    
    // Each charity claims their share (0.7 ETH / 3 = ~0.233 ETH each)
    const proof1 = tree.getProof([0, charity1.address]);
    const proof2 = tree.getProof([1, charity2.address]);
    const proof3 = tree.getProof([2, charity3.address]);
    
    const charity1Before = await ethers.provider.getBalance(charity1.address);
    const charity2Before = await ethers.provider.getBalance(charity2.address);
    const charity3Before = await ethers.provider.getBalance(charity3.address);
    
    await distributor.claim(0, charity1.address, proof1);
    await distributor.claim(1, charity2.address, proof2);
    await distributor.claim(2, charity3.address, proof3);
    
    const charity1After = await ethers.provider.getBalance(charity1.address);
    const charity2After = await ethers.provider.getBalance(charity2.address);
    const charity3After = await ethers.provider.getBalance(charity3.address);
    
    const expectedShare = expectedCharity / 3n;
    
    expect(charity1After - charity1Before).to.equal(expectedShare);
    expect(charity2After - charity2Before).to.equal(expectedShare);
    expect(charity3After - charity3Before).to.equal(expectedShare);
    
    // Verify all claimed
    const [, claimed, , ] = await distributor.getStats();
    expect(claimed).to.equal(expectedShare * 3n);
  });

  it("Should handle multiple distributions over time", async function () {
    const { splitter, distributor, tree, charity1, user } = await loadFixture(deployFullSystemFixture);
    
    // First distribution
    await user.sendTransaction({
      to: await splitter.getAddress(),
      value: ethers.parseEther("10.0")
    });
    
    const proof1 = tree.getProof([0, charity1.address]);
    await distributor.claim(0, charity1.address, proof1);
    
    // Second distribution
    await user.sendTransaction({
      to: await splitter.getAddress(),
      value: ethers.parseEther("5.0")
    });
    
    // Charity can claim again in new epoch
    await distributor.claim(0, charity1.address, proof1);
    
    // Total received should be 15 ETH * 7% = 1.05 ETH
    expect(await distributor.totalReceived()).to.equal(ethers.parseEther("1.05"));
  });
});
