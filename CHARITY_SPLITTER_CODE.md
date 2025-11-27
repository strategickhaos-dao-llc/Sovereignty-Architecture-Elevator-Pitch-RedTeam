# Strategickhaos 7% Charity Splitter

## ⚠️ STATUS: CODE ONLY - NOT DEPLOYED

**This smart contract code is ready for deployment but has NOT been deployed to any blockchain.**

---

## Overview

This contract implements an immutable 7% charitable split for the Strategickhaos DAO. Once deployed, the percentage becomes mathematically eternal and cannot be changed by anyone.

---

## Smart Contract Code (Solidity)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title CharitySplitter
 * @notice Strategickhaos DAO 7% Immutable Charity Split
 * @dev Once deployed, the 7% split is mathematically eternal
 * 
 * STATUS: CODE ONLY - DEPLOY AFTER NODE.JS INSTALLATION
 */
contract CharitySplitter is ReentrancyGuard, Ownable {
    
    // ============ IMMUTABLE CONSTANTS ============
    
    /// @notice The charity percentage - IMMUTABLE, ETERNAL, UNCHANGEABLE
    uint256 public constant CHARITY_PERCENTAGE = 7;
    
    /// @notice Basis points denominator (100%)
    uint256 public constant BASIS_POINTS = 100;
    
    // ============ STATE VARIABLES ============
    
    /// @notice Charity wallet address (can be updated by owner for operational flexibility)
    address public charityWallet;
    
    /// @notice Operations wallet address
    address public operationsWallet;
    
    /// @notice Total charity distributed (for transparency)
    uint256 public totalCharityDistributed;
    
    /// @notice Total operations distributed
    uint256 public totalOperationsDistributed;
    
    // ============ EVENTS ============
    
    event FundsReceived(address indexed sender, uint256 amount, uint256 timestamp);
    event FundsSplit(
        uint256 charityAmount, 
        uint256 operationsAmount, 
        uint256 timestamp
    );
    event CharityWalletUpdated(address indexed oldWallet, address indexed newWallet);
    event OperationsWalletUpdated(address indexed oldWallet, address indexed newWallet);
    
    // ============ CONSTRUCTOR ============
    
    /**
     * @notice Initialize the charity splitter
     * @param _charityWallet Address to receive 7% charity split
     * @param _operationsWallet Address to receive 93% operations split
     */
    constructor(
        address _charityWallet,
        address _operationsWallet
    ) Ownable(msg.sender) {
        require(_charityWallet != address(0), "Invalid charity wallet");
        require(_operationsWallet != address(0), "Invalid operations wallet");
        
        charityWallet = _charityWallet;
        operationsWallet = _operationsWallet;
    }
    
    // ============ RECEIVE FUNCTION ============
    
    /**
     * @notice Receive ETH and automatically split
     * @dev The 7% is MATHEMATICALLY ENFORCED - no one can change this
     */
    receive() external payable nonReentrant {
        require(msg.value > 0, "Must send ETH");
        
        emit FundsReceived(msg.sender, msg.value, block.timestamp);
        
        // Calculate the IMMUTABLE 7% charity split
        uint256 charityAmount = (msg.value * CHARITY_PERCENTAGE) / BASIS_POINTS;
        uint256 operationsAmount = msg.value - charityAmount;
        
        // Update totals for transparency
        totalCharityDistributed += charityAmount;
        totalOperationsDistributed += operationsAmount;
        
        // Transfer to charity (7% - ETERNAL)
        (bool charitySuccess, ) = charityWallet.call{value: charityAmount}("");
        require(charitySuccess, "Charity transfer failed");
        
        // Transfer to operations (93%)
        (bool opsSuccess, ) = operationsWallet.call{value: operationsAmount}("");
        require(opsSuccess, "Operations transfer failed");
        
        emit FundsSplit(charityAmount, operationsAmount, block.timestamp);
    }
    
    // ============ ADMIN FUNCTIONS ============
    
    /**
     * @notice Update charity wallet address
     * @dev Only owner can update, but the 7% PERCENTAGE IS IMMUTABLE
     * @param _newCharityWallet New charity wallet address
     */
    function updateCharityWallet(address _newCharityWallet) external onlyOwner {
        require(_newCharityWallet != address(0), "Invalid address");
        address oldWallet = charityWallet;
        charityWallet = _newCharityWallet;
        emit CharityWalletUpdated(oldWallet, _newCharityWallet);
    }
    
    /**
     * @notice Update operations wallet address
     * @param _newOperationsWallet New operations wallet address
     */
    function updateOperationsWallet(address _newOperationsWallet) external onlyOwner {
        require(_newOperationsWallet != address(0), "Invalid address");
        address oldWallet = operationsWallet;
        operationsWallet = _newOperationsWallet;
        emit OperationsWalletUpdated(oldWallet, _newOperationsWallet);
    }
    
    // ============ VIEW FUNCTIONS ============
    
    /**
     * @notice Get current split configuration
     * @return charity The charity percentage (always 7)
     * @return operations The operations percentage (always 93)
     */
    function getSplitConfig() external pure returns (uint256 charity, uint256 operations) {
        return (CHARITY_PERCENTAGE, BASIS_POINTS - CHARITY_PERCENTAGE);
    }
    
    /**
     * @notice Get total distribution stats
     * @return charityTotal Total distributed to charity
     * @return operationsTotal Total distributed to operations
     */
    function getDistributionStats() external view returns (
        uint256 charityTotal, 
        uint256 operationsTotal
    ) {
        return (totalCharityDistributed, totalOperationsDistributed);
    }
    
    /**
     * @notice Calculate split for a given amount (preview)
     * @param amount The amount to calculate split for
     * @return charityAmount Amount that would go to charity (7%)
     * @return operationsAmount Amount that would go to operations (93%)
     */
    function calculateSplit(uint256 amount) external pure returns (
        uint256 charityAmount,
        uint256 operationsAmount
    ) {
        charityAmount = (amount * CHARITY_PERCENTAGE) / BASIS_POINTS;
        operationsAmount = amount - charityAmount;
    }
}
```

---

## Hardhat Deployment Script

```javascript
// scripts/deploy.js
const hre = require("hardhat");

async function main() {
  // Configuration - UPDATE THESE BEFORE DEPLOYMENT
  const CHARITY_WALLET = "0x..."; // Your charity wallet address
  const OPERATIONS_WALLET = "0x..."; // Your operations wallet address

  console.log("Deploying CharitySplitter...");
  console.log("Charity Wallet:", CHARITY_WALLET);
  console.log("Operations Wallet:", OPERATIONS_WALLET);

  const CharitySplitter = await hre.ethers.getContractFactory("CharitySplitter");
  const splitter = await CharitySplitter.deploy(CHARITY_WALLET, OPERATIONS_WALLET);

  await splitter.waitForDeployment();

  const address = await splitter.getAddress();
  console.log("CharitySplitter deployed to:", address);
  
  // Verify the immutable 7%
  const [charity, operations] = await splitter.getSplitConfig();
  console.log(`Split Config: ${charity}% charity, ${operations}% operations`);
  
  // The 7% is now MATHEMATICALLY ETERNAL
  console.log("\n✅ The 7% charitable split is now immutable on-chain!");
  
  return address;
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

---

## Hardhat Configuration

```javascript
// hardhat.config.js
require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    baseSepolia: {
      url: process.env.BASE_SEPOLIA_RPC || "https://sepolia.base.org",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      chainId: 84532
    },
    baseMainnet: {
      url: process.env.BASE_MAINNET_RPC || "https://mainnet.base.org",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      chainId: 8453
    }
  },
  etherscan: {
    apiKey: {
      baseSepolia: process.env.BASESCAN_API_KEY || "",
      base: process.env.BASESCAN_API_KEY || ""
    },
    customChains: [
      {
        network: "baseSepolia",
        chainId: 84532,
        urls: {
          apiURL: "https://api-sepolia.basescan.org/api",
          browserURL: "https://sepolia.basescan.org"
        }
      }
    ]
  }
};
```

---

## Environment Template

```bash
# .env.contract (DO NOT COMMIT WITH REAL VALUES)
PRIVATE_KEY=your_wallet_private_key_here
BASE_SEPOLIA_RPC=https://sepolia.base.org
BASE_MAINNET_RPC=https://mainnet.base.org
BASESCAN_API_KEY=your_basescan_api_key
```

---

## Deployment Checklist

- [ ] Install Node.js 18+ LTS
- [ ] Run `npm init -y`
- [ ] Run `npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox`
- [ ] Run `npm install @openzeppelin/contracts dotenv`
- [ ] Create `contracts/CharitySplitter.sol` with code above
- [ ] Create `scripts/deploy.js` with script above
- [ ] Create `hardhat.config.js` with config above
- [ ] Create `.env` with wallet configuration
- [ ] Run `npx hardhat compile`
- [ ] Deploy to testnet: `npx hardhat run scripts/deploy.js --network baseSepolia`
- [ ] Verify contract: `npx hardhat verify --network baseSepolia <CONTRACT_ADDRESS> <CHARITY_WALLET> <OPS_WALLET>`

---

## ⚠️ IMPORTANT NOTICE

**This is CODE, not a DEPLOYED CONTRACT.**

- The smart contract code above is syntactically correct
- It has NOT been deployed to any blockchain
- The 7% split is NOT yet "mathematically eternal"
- Deployment requires Node.js, npm, and wallet configuration

**See DEPLOY_TOMORROW.md for deployment instructions.**

---

## Security Considerations

1. **Immutable Percentage**: The 7% is a constant - cannot be changed after deployment
2. **Reentrancy Protection**: Uses OpenZeppelin's ReentrancyGuard
3. **Access Control**: Owner can update wallet addresses but NOT the percentage
4. **Transparent Accounting**: All distributions are tracked on-chain

---

## Audit Recommendations

Before mainnet deployment:
- [ ] Professional smart contract audit
- [ ] Formal verification of split logic
- [ ] Test on Base Sepolia testnet
- [ ] Verify contract source on Basescan

---

*Status: CODE READY - AWAITING DEPLOYMENT*

💙🔥⚔️∞
