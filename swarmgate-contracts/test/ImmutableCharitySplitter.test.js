const { expect } = require("chai");
const { ethers } = require("hardhat");
const { loadFixture, time } = require("@nomicfoundation/hardhat-toolbox/network-helpers");

describe("ImmutableCharitySplitter", function () {
  // Deploy fixture for reuse across tests
  async function deployCharitySplitterFixture() {
    const [owner, opsMultisig, charity1, charity2, charity3, sender] = await ethers.getSigners();

    const charities = [charity1.address, charity2.address, charity3.address];

    const CharitySplitter = await ethers.getContractFactory("ImmutableCharitySplitter");
    const splitter = await CharitySplitter.deploy(opsMultisig.address, charities);

    return { splitter, owner, opsMultisig, charity1, charity2, charity3, sender, charities };
  }

  describe("Deployment", function () {
    it("Should set the correct ops multisig address", async function () {
      const { splitter, opsMultisig } = await loadFixture(deployCharitySplitterFixture);
      expect(await splitter.operationalMultisig()).to.equal(opsMultisig.address);
    });

    it("Should set the correct charity addresses", async function () {
      const { splitter, charity1, charity2, charity3 } = await loadFixture(deployCharitySplitterFixture);
      expect(await splitter.charities(0)).to.equal(charity1.address);
      expect(await splitter.charities(1)).to.equal(charity2.address);
      expect(await splitter.charities(2)).to.equal(charity3.address);
    });

    it("Should revert on zero address for ops multisig", async function () {
      const [_, charity1] = await ethers.getSigners();
      const CharitySplitter = await ethers.getContractFactory("ImmutableCharitySplitter");
      await expect(
        CharitySplitter.deploy(ethers.ZeroAddress, [charity1.address])
      ).to.be.revertedWithCustomError(CharitySplitter, "InvalidConfiguration");
    });

    it("Should revert on empty charities array", async function () {
      const [_, opsMultisig] = await ethers.getSigners();
      const CharitySplitter = await ethers.getContractFactory("ImmutableCharitySplitter");
      await expect(
        CharitySplitter.deploy(opsMultisig.address, [])
      ).to.be.revertedWithCustomError(CharitySplitter, "InvalidConfiguration");
    });

    it("Should have correct constant values", async function () {
      const { splitter } = await loadFixture(deployCharitySplitterFixture);
      expect(await splitter.CHARITY_BPS()).to.equal(700n);  // 7%
      expect(await splitter.OPS_BPS()).to.equal(9300n);      // 93%
      expect(await splitter.BPS_DENOMINATOR()).to.equal(10000n);
    });
  });

  describe("Payment Splitting", function () {
    it("Should split payments exactly 7% to charity, 93% to ops", async function () {
      const { splitter, opsMultisig, sender } = await loadFixture(deployCharitySplitterFixture);

      const payment = ethers.parseEther("100");
      const expectedCharity = ethers.parseEther("7");    // 7%
      const expectedOps = ethers.parseEther("93");       // 93%

      const opsBalanceBefore = await ethers.provider.getBalance(opsMultisig.address);

      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: payment,
      });

      const opsBalanceAfter = await ethers.provider.getBalance(opsMultisig.address);
      const contractBalance = await ethers.provider.getBalance(await splitter.getAddress());

      // Verify 93% went to ops
      expect(opsBalanceAfter - opsBalanceBefore).to.equal(expectedOps);

      // Verify 7% is held in contract for charity
      expect(contractBalance).to.equal(expectedCharity);

      // Verify accounting
      expect(await splitter.totalCharityRaised()).to.equal(expectedCharity);
      expect(await splitter.totalOpsForwarded()).to.equal(expectedOps);
    });

    it("Should handle small amounts correctly", async function () {
      const { splitter, opsMultisig, sender } = await loadFixture(deployCharitySplitterFixture);

      const payment = ethers.parseEther("1");
      const expectedCharity = ethers.parseEther("0.07");  // 7%
      const expectedOps = ethers.parseEther("0.93");      // 93%

      const opsBalanceBefore = await ethers.provider.getBalance(opsMultisig.address);

      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: payment,
      });

      const opsBalanceAfter = await ethers.provider.getBalance(opsMultisig.address);
      const contractBalance = await ethers.provider.getBalance(await splitter.getAddress());

      expect(opsBalanceAfter - opsBalanceBefore).to.equal(expectedOps);
      expect(contractBalance).to.equal(expectedCharity);
    });

    it("Should handle very small amounts (wei precision)", async function () {
      const { splitter, opsMultisig, sender } = await loadFixture(deployCharitySplitterFixture);

      // 10000 wei - should split exactly
      const payment = 10000n;
      const expectedCharity = 700n;   // 7%
      const expectedOps = 9300n;      // 93%

      const opsBalanceBefore = await ethers.provider.getBalance(opsMultisig.address);

      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: payment,
      });

      const opsBalanceAfter = await ethers.provider.getBalance(opsMultisig.address);
      const contractBalance = await ethers.provider.getBalance(await splitter.getAddress());

      expect(opsBalanceAfter - opsBalanceBefore).to.equal(expectedOps);
      expect(contractBalance).to.equal(expectedCharity);
    });

    it("Should emit PaymentReceived and OpsForwarded events", async function () {
      const { splitter, opsMultisig, sender } = await loadFixture(deployCharitySplitterFixture);

      const payment = ethers.parseEther("10");
      const charityShare = ethers.parseEther("0.7");
      const opsShare = ethers.parseEther("9.3");

      await expect(
        sender.sendTransaction({
          to: await splitter.getAddress(),
          value: payment,
        })
      )
        .to.emit(splitter, "PaymentReceived")
        .withArgs(sender.address, payment, charityShare, opsShare)
        .and.to.emit(splitter, "OpsForwarded")
        .withArgs(opsMultisig.address, opsShare);
    });

    it("Should not do anything for zero value transfers", async function () {
      const { splitter, sender } = await loadFixture(deployCharitySplitterFixture);

      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: 0n,
      });

      expect(await splitter.totalCharityRaised()).to.equal(0n);
      expect(await splitter.totalOpsForwarded()).to.equal(0n);
    });

    it("Should accumulate multiple payments correctly", async function () {
      const { splitter, opsMultisig, sender } = await loadFixture(deployCharitySplitterFixture);

      // First payment: 10 ETH
      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: ethers.parseEther("10"),
      });

      // Second payment: 20 ETH
      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: ethers.parseEther("20"),
      });

      // Total: 30 ETH -> 2.1 ETH charity (7%), 27.9 ETH ops (93%)
      expect(await splitter.totalCharityRaised()).to.equal(ethers.parseEther("2.1"));
      expect(await splitter.totalOpsForwarded()).to.equal(ethers.parseEther("27.9"));

      // Contract should hold the charity balance
      expect(await splitter.pendingCharityBalance()).to.equal(ethers.parseEther("2.1"));
    });
  });

  describe("Charity Distribution", function () {
    it("Should revert if distribution interval not met", async function () {
      const { splitter, sender } = await loadFixture(deployCharitySplitterFixture);

      // Send some funds first
      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: ethers.parseEther("10"),
      });

      // Try to distribute immediately
      await expect(splitter.distributeCharity())
        .to.be.revertedWithCustomError(splitter, "DistributionTooEarly");
    });

    it("Should revert if no funds to distribute", async function () {
      const { splitter } = await loadFixture(deployCharitySplitterFixture);

      // Advance time past distribution interval
      await time.increase(91 * 24 * 60 * 60); // 91 days

      await expect(splitter.distributeCharity())
        .to.be.revertedWithCustomError(splitter, "NoFundsToDistribute");
    });

    it("Should distribute funds equally to all charities after interval", async function () {
      const { splitter, charity1, charity2, charity3, sender } = await loadFixture(deployCharitySplitterFixture);

      // Send 300 ETH -> 21 ETH to charity (7%)
      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: ethers.parseEther("300"),
      });

      const expectedCharityBalance = ethers.parseEther("21"); // 7% of 300
      expect(await splitter.pendingCharityBalance()).to.equal(expectedCharityBalance);

      // Get initial balances
      const c1BalanceBefore = await ethers.provider.getBalance(charity1.address);
      const c2BalanceBefore = await ethers.provider.getBalance(charity2.address);
      const c3BalanceBefore = await ethers.provider.getBalance(charity3.address);

      // Advance time past distribution interval
      await time.increase(91 * 24 * 60 * 60); // 91 days

      // Distribute
      await expect(splitter.distributeCharity())
        .to.emit(splitter, "CharityDistributed");

      // Each charity should receive 7 ETH (21 / 3)
      const sharePerCharity = ethers.parseEther("7");

      const c1BalanceAfter = await ethers.provider.getBalance(charity1.address);
      const c2BalanceAfter = await ethers.provider.getBalance(charity2.address);
      const c3BalanceAfter = await ethers.provider.getBalance(charity3.address);

      expect(c1BalanceAfter - c1BalanceBefore).to.equal(sharePerCharity);
      expect(c2BalanceAfter - c2BalanceBefore).to.equal(sharePerCharity);
      expect(c3BalanceAfter - c3BalanceBefore).to.equal(sharePerCharity);
    });

    it("Should reset lastDistributionTime after distribution", async function () {
      const { splitter, sender } = await loadFixture(deployCharitySplitterFixture);

      // Send funds
      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: ethers.parseEther("30"),
      });

      // Advance time and distribute
      await time.increase(91 * 24 * 60 * 60);
      await splitter.distributeCharity();

      // Try to distribute again immediately - should fail
      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: ethers.parseEther("30"),
      });

      await expect(splitter.distributeCharity())
        .to.be.revertedWithCustomError(splitter, "DistributionTooEarly");
    });

    it("Should allow anyone to call distributeCharity (keeper friendly)", async function () {
      const { splitter, sender, charity1 } = await loadFixture(deployCharitySplitterFixture);

      // Send funds
      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: ethers.parseEther("30"),
      });

      // Advance time
      await time.increase(91 * 24 * 60 * 60);

      // Have charity1 (any random account) call distribute
      await expect(splitter.connect(charity1).distributeCharity()).to.not.be.reverted;
    });
  });

  describe("View Functions", function () {
    it("Should return correct pending charity balance", async function () {
      const { splitter, sender } = await loadFixture(deployCharitySplitterFixture);

      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: ethers.parseEther("100"),
      });

      expect(await splitter.pendingCharityBalance()).to.equal(ethers.parseEther("7"));
    });

    it("Should track total charity raised correctly", async function () {
      const { splitter, sender } = await loadFixture(deployCharitySplitterFixture);

      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: ethers.parseEther("100"),
      });

      expect(await splitter.totalCharityRaised()).to.equal(ethers.parseEther("7"));
    });

    it("Should track total ops forwarded correctly", async function () {
      const { splitter, sender } = await loadFixture(deployCharitySplitterFixture);

      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: ethers.parseEther("100"),
      });

      expect(await splitter.totalOpsForwarded()).to.equal(ethers.parseEther("93"));
    });
  });

  describe("Math Precision Tests", function () {
    it("7% calculation should be exact for amounts divisible by 10000", async function () {
      const { splitter, sender } = await loadFixture(deployCharitySplitterFixture);

      // 10000 wei - perfectly divisible
      const payment = 10000n;
      
      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: payment,
      });

      // 7% of 10000 = 700
      expect(await splitter.totalCharityRaised()).to.equal(700n);
      // 93% of 10000 = 9300
      expect(await splitter.totalOpsForwarded()).to.equal(9300n);
    });

    it("Should handle remainders correctly (ops gets remainder to avoid dust)", async function () {
      const { splitter, sender } = await loadFixture(deployCharitySplitterFixture);

      // 10001 wei - not perfectly divisible
      const payment = 10001n;
      
      await sender.sendTransaction({
        to: await splitter.getAddress(),
        value: payment,
      });

      // 7% of 10001 = 700.07 -> truncates to 700
      const charityShare = (payment * 700n) / 10000n; // 700
      // Ops gets remainder: 10001 - 700 = 9301
      const opsShare = payment - charityShare;

      expect(await splitter.totalCharityRaised()).to.equal(700n);
      expect(await splitter.totalOpsForwarded()).to.equal(9301n);
    });

    it("Sum of charity + ops should always equal input", async function () {
      const { splitter, sender } = await loadFixture(deployCharitySplitterFixture);

      // Test with various amounts
      const testAmounts = [
        ethers.parseEther("1"),
        ethers.parseEther("0.001"),
        ethers.parseEther("123.456789"),
        12345n,
        99999n,
      ];

      for (const payment of testAmounts) {
        const { splitter: freshSplitter } = await loadFixture(deployCharitySplitterFixture);
        
        await sender.sendTransaction({
          to: await freshSplitter.getAddress(),
          value: payment,
        });

        const charity = await freshSplitter.totalCharityRaised();
        const ops = await freshSplitter.totalOpsForwarded();

        expect(charity + ops).to.equal(payment);
      }
    });
  });
});
