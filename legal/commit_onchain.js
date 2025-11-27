/**
 * On-Chain Commit Transaction Script for Legal Shield Bundle
 * 
 * This script commits the BLAKE3 hash and IPFS CID of the legal shield bundle
 * to a CommitRegistry smart contract on Base L2.
 * 
 * Prerequisites:
 *   npm install ethers
 * 
 * Usage:
 *   1. Replace placeholders with actual values
 *   2. Run: node commit_onchain.js
 * 
 * Security:
 *   - NEVER commit private keys to version control
 *   - Use environment variables or a secure key management system
 */

const ethers = require('ethers');

// Configuration - Replace with actual values before use
const CONFIG = {
  // Base L2 RPC endpoint (mainnet or testnet)
  rpcUrl: process.env.BASE_RPC_URL || 'https://mainnet.base.org',
  
  // Private key - MUST be set via environment variable
  privateKey: process.env.PRIVATE_KEY || 'REPLACE_WITH_YOUR_PRIVATE_KEY',
  
  // CommitRegistry contract address - REPLACE with deployed address
  contractAddress: process.env.CONTRACT_ADDRESS || '0x_REPLACE_WITH_DEPLOYED_CONTRACT_ADDRESS',
  
  // BLAKE3 hash of bundle.tar (computed via compute_hash.py)
  blake3Hash: process.env.BLAKE3_HASH || 'REPLACE_WITH_COMPUTED_BLAKE3_HASH',
  
  // IPFS CID of uploaded bundle
  ipfsCid: process.env.IPFS_CID || 'REPLACE_WITH_IPFS_CID',
  
  // Commit tag
  tag: 'LegalShield-v1.0'
};

// CommitRegistry ABI (minimal)
const COMMIT_REGISTRY_ABI = [
  'function commit(bytes32 b3Hash, string memory ipfsCid, string memory tag)'
];

async function commitLegalShield() {
  console.log('Connecting to Base L2...');
  
  // Create provider and wallet
  const provider = new ethers.providers.JsonRpcProvider(CONFIG.rpcUrl);
  const wallet = new ethers.Wallet(CONFIG.privateKey, provider);
  
  console.log(`Wallet address: ${wallet.address}`);
  
  // Create contract instance
  const contract = new ethers.Contract(
    CONFIG.contractAddress,
    COMMIT_REGISTRY_ABI,
    wallet
  );
  
  // Format hash as bytes32
  const b3Hash = CONFIG.blake3Hash.startsWith('0x') 
    ? CONFIG.blake3Hash 
    : '0x' + CONFIG.blake3Hash;
  
  console.log('\nCommitting to CommitRegistry:');
  console.log(`  Hash: ${b3Hash}`);
  console.log(`  IPFS CID: ${CONFIG.ipfsCid}`);
  console.log(`  Tag: ${CONFIG.tag}`);
  
  // Execute commit transaction
  const tx = await contract.commit(b3Hash, CONFIG.ipfsCid, CONFIG.tag);
  console.log(`\nTransaction submitted: ${tx.hash}`);
  
  // Wait for confirmation
  const receipt = await tx.wait();
  console.log(`Transaction confirmed in block: ${receipt.blockNumber}`);
  console.log(`Transaction hash: ${receipt.transactionHash}`);
  console.log(`Gas used: ${receipt.gasUsed.toString()}`);
  
  return receipt;
}

// Execute
commitLegalShield()
  .then(() => {
    console.log('\nLegal shield committed successfully!');
    process.exit(0);
  })
  .catch((error) => {
    console.error('\nError committing legal shield:', error.message);
    process.exit(1);
  });
