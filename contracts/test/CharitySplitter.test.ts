import { expect } from "chai";
import { ethers } from "hardhat";
import { IrrevocableCharitySplitter, MerkleCharityDistributor } from "../typechain-types";
import { SignerWithAddress } from "@nomicfoundation/hardhat-ethers/signers";
import { MerkleTree } from "merkletreejs";
import keccak256 from "keccak256";

describe("IrrevocableCharitySplitter", function () {
  let splitter: IrrevocableCharitySplitter;
  let distributor: MerkleCharityDistributor;
  let owner: SignerWithAddress;
  let operationsMultisig: SignerWithAddress;
  let charity1: SignerWithAddress;
  let charity2: SignerWithAddress;
  let user: SignerWithAddress;

  const CHARITY_BPS = 700n; // 7%
  const OPERATIONS_BPS = 9300n; // 93%
  const TOTAL_BPS = 10000n;

  beforeEach(async function () {
    [owner, operationsMultisig, charity1, charity2, user] = await ethers.getSigners();

    // Deploy MerkleCharityDistributor first
    const MerkleCharityDistributor = await ethers.getContractFactory("MerkleCharityDistributor");
    distributor = await MerkleCharityDistributor.deploy(owner.address);
    await distributor.waitForDeployment();

    // Deploy IrrevocableCharitySplitter
    const IrrevocableCharitySplitter = await ethers.getContractFactory("IrrevocableCharitySplitter");
    splitter = await IrrevocableCharitySplitter.deploy(
      operationsMultisig.address,
      await distributor.getAddress()
    );
    await splitter.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the correct operations multisig", async function () {
      expect(await splitter.operationsMultisig()).to.equal(operationsMultisig.address);
    });

    it("Should set the correct charity treasury", async function () {
      expect(await splitter.charityTreasury()).to.equal(await distributor.getAddress());
    });

    it("Should have correct charity percentage (7%)", async function () {
      expect(await splitter.CHARITY_BPS()).to.equal(CHARITY_BPS);
    });

    it("Should have correct operations percentage (93%)", async function () {
      expect(await splitter.OPERATIONS_BPS()).to.equal(OPERATIONS_BPS);
    });

    it("Should verify charity percentage returns true", async function () {
      expect(await splitter.verifyCharityPercentage()).to.be.true;
    });

    it("Should emit SplitterDeployed event", async function () {
      const IrrevocableCharitySplitter = await ethers.getContractFactory("IrrevocableCharitySplitter");
      const tx = IrrevocableCharitySplitter.deploy(
        operationsMultisig.address,
        await distributor.getAddress()
      );
      
      await expect(tx).to.emit(await tx, "SplitterDeployed");
    });

    it("Should revert with zero address for operations", async function () {
      const IrrevocableCharitySplitter = await ethers.getContractFactory("IrrevocableCharitySplitter");
      await expect(
        IrrevocableCharitySplitter.deploy(ethers.ZeroAddress, await distributor.getAddress())
      ).to.be.revertedWithCustomError(splitter, "ZeroAddress");
    });

    it("Should revert with zero address for charity", async function () {
      const IrrevocableCharitySplitter = await ethers.getContractFactory("IrrevocableCharitySplitter");
      await expect(
        IrrevocableCharitySplitter.deploy(operationsMultisig.address, ethers.ZeroAddress)
      ).to.be.revertedWithCustomError(splitter, "ZeroAddress");
    });
  });

  describe("ETH Splitting", function () {
    it("Should split incoming ETH correctly (7% charity, 93% operations)", async function () {
      const amount = ethers.parseEther("100");
      const expectedCharity = (amount * CHARITY_BPS) / TOTAL_BPS;
      const expectedOperations = amount - expectedCharity;

      const distributorAddress = await distributor.getAddress();
      const initialCharityBalance = await ethers.provider.getBalance(distributorAddress);
      const initialOpsBalance = await ethers.provider.getBalance(operationsMultisig.address);

      // Send ETH to splitter
      await user.sendTransaction({
        to: await splitter.getAddress(),
        value: amount,
      });

      const finalCharityBalance = await ethers.provider.getBalance(distributorAddress);
      const finalOpsBalance = await ethers.provider.getBalance(operationsMultisig.address);

      expect(finalCharityBalance - initialCharityBalance).to.equal(expectedCharity);
      expect(finalOpsBalance - initialOpsBalance).to.equal(expectedOperations);
    });

    it("Should emit EthSplit event with correct values", async function () {
      const amount = ethers.parseEther("10");
      const expectedCharity = (amount * CHARITY_BPS) / TOTAL_BPS;
      const expectedOperations = amount - expectedCharity;

      await expect(
        user.sendTransaction({
          to: await splitter.getAddress(),
          value: amount,
        })
      )
        .to.emit(splitter, "EthSplit")
        .withArgs(
          (val: bigint) => val > 0, // timestamp
          amount,
          expectedCharity,
          expectedOperations
        );
    });

    it("Should update statistics correctly", async function () {
      const amount1 = ethers.parseEther("50");
      const amount2 = ethers.parseEther("30");

      await user.sendTransaction({
        to: await splitter.getAddress(),
        value: amount1,
      });

      await user.sendTransaction({
        to: await splitter.getAddress(),
        value: amount2,
      });

      const totalReceived = amount1 + amount2;
      const expectedCharity = (totalReceived * CHARITY_BPS) / TOTAL_BPS;
      const expectedOperations = totalReceived - expectedCharity;

      const [received, toCharity, toOperations] = await splitter.getEthStats();
      expect(received).to.equal(totalReceived);
      expect(toCharity).to.equal(expectedCharity);
      expect(toOperations).to.equal(expectedOperations);
    });

    it("Should handle small amounts correctly", async function () {
      const amount = ethers.parseEther("0.001"); // Small amount
      const expectedCharity = (amount * CHARITY_BPS) / TOTAL_BPS;

      const distributorAddress = await distributor.getAddress();
      const initialCharityBalance = await ethers.provider.getBalance(distributorAddress);

      await user.sendTransaction({
        to: await splitter.getAddress(),
        value: amount,
      });

      const finalCharityBalance = await ethers.provider.getBalance(distributorAddress);
      expect(finalCharityBalance - initialCharityBalance).to.equal(expectedCharity);
    });

    it("Should allow anyone to trigger splitEthBalance", async function () {
      // First, we need to somehow get ETH to the contract without triggering receive()
      // This is a special case - normally receive() would split immediately
      // This test verifies the splitEthBalance function works if called directly
      
      // For this test, we'll verify the function reverts when no balance
      await expect(splitter.connect(user).splitEthBalance()).to.be.revertedWithCustomError(
        splitter,
        "NoFundsToSplit"
      );
    });
  });

  describe("Immutability", function () {
    it("Should not have any admin functions", async function () {
      // Verify there are no state-changing admin functions
      // The contract should have no owner, admin, or governance functions
      const splitterInterface = splitter.interface;
      
      // Check that there's no setCharity, setOperations, pause, upgrade functions
      expect(splitterInterface.hasFunction("setCharityTreasury")).to.be.false;
      expect(splitterInterface.hasFunction("setOperationsMultisig")).to.be.false;
      expect(splitterInterface.hasFunction("pause")).to.be.false;
      expect(splitterInterface.hasFunction("unpause")).to.be.false;
      expect(splitterInterface.hasFunction("upgrade")).to.be.false;
      expect(splitterInterface.hasFunction("setCharityPercentage")).to.be.false;
    });

    it("Charity percentage should be constant", async function () {
      // Verify CHARITY_BPS is a constant (read multiple times should return same value)
      const bps1 = await splitter.CHARITY_BPS();
      const bps2 = await splitter.CHARITY_BPS();
      expect(bps1).to.equal(bps2);
      expect(bps1).to.equal(700n);
    });
  });
});

describe("MerkleCharityDistributor", function () {
  let distributor: MerkleCharityDistributor;
  let owner: SignerWithAddress;
  let charity1: SignerWithAddress;
  let charity2: SignerWithAddress;
  let user: SignerWithAddress;

  beforeEach(async function () {
    [owner, charity1, charity2, user] = await ethers.getSigners();

    const MerkleCharityDistributor = await ethers.getContractFactory("MerkleCharityDistributor");
    distributor = await MerkleCharityDistributor.deploy(owner.address);
    await distributor.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the correct root updater", async function () {
      expect(await distributor.rootUpdater()).to.equal(owner.address);
    });

    it("Should start at epoch 0", async function () {
      expect(await distributor.currentEpoch()).to.equal(0);
    });

    it("Should have 90 day distribution interval", async function () {
      expect(await distributor.DISTRIBUTION_INTERVAL()).to.equal(90 * 24 * 60 * 60);
    });
  });

  describe("Charity Registration", function () {
    it("Should allow root updater to register charities", async function () {
      await expect(
        distributor.registerCharity(
          charity1.address,
          "Against Malaria Foundation",
          "20-8521450",
          2500
        )
      )
        .to.emit(distributor, "CharityRegistered")
        .withArgs(charity1.address, "Against Malaria Foundation", "20-8521450", 2500);
    });

    it("Should not allow non-root-updater to register charities", async function () {
      await expect(
        distributor.connect(user).registerCharity(
          charity1.address,
          "Test Charity",
          "12-3456789",
          2500
        )
      ).to.be.revertedWithCustomError(distributor, "NotRootUpdater");
    });

    it("Should not allow duplicate charity registration", async function () {
      await distributor.registerCharity(charity1.address, "Charity 1", "12-3456789", 2500);
      
      await expect(
        distributor.registerCharity(charity1.address, "Charity 1 Again", "12-3456789", 2500)
      ).to.be.revertedWithCustomError(distributor, "CharityAlreadyRegistered");
    });

    it("Should track all registered charities", async function () {
      await distributor.registerCharity(charity1.address, "Charity 1", "11-1111111", 5000);
      await distributor.registerCharity(charity2.address, "Charity 2", "22-2222222", 5000);

      expect(await distributor.getCharityCount()).to.equal(2);
      
      const charities = await distributor.getAllCharities();
      expect(charities).to.include(charity1.address);
      expect(charities).to.include(charity2.address);
    });
  });

  describe("Treasury Balance", function () {
    it("Should accept ETH deposits", async function () {
      const amount = ethers.parseEther("10");
      
      await user.sendTransaction({
        to: await distributor.getAddress(),
        value: amount,
      });

      expect(await distributor.getTreasuryBalance()).to.equal(amount);
    });
  });
});
