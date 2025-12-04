/**
 * On-Chain Commit Transaction Script using Viem (Alternative to ethers.js)
 * 
 * This script commits the BLAKE3 hash and IPFS CID of the legal shield bundle
 * to a CommitRegistry smart contract on Base L2 using the viem library.
 * 
 * Prerequisites:
 *   npm install viem
 * 
 * Usage:
 *   1. Replace placeholders with actual values
 *   2. Run: node commit_onchain_viem.mjs
 * 
 * Security:
 *   - NEVER commit private keys to version control
 *   - Use environment variables or a secure key management system
 */

import { createWalletClient, http, parseAbi } from 'viem';
import { base, baseSepolia } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';

// Configuration - Replace with actual values before use
const CONFIG = {
  // Use baseSepolia for testnet, base for mainnet
  chain: process.env.USE_TESTNET === 'true' ? baseSepolia : base,
  
  // Private key - MUST be set via environment variable
  privateKey: process.env.PRIVATE_KEY || '0x_REPLACE_WITH_YOUR_PRIVATE_KEY',
  
  // CommitRegistry contract address - REPLACE with deployed address
  contractAddress: process.env.CONTRACT_ADDRESS || '0x_REPLACE_WITH_DEPLOYED_CONTRACT_ADDRESS',
  
  // BLAKE3 hash of bundle.tar (computed via compute_hash.py)
  blake3Hash: process.env.BLAKE3_HASH || '0x_REPLACE_WITH_COMPUTED_BLAKE3_HASH',
  
  // IPFS CID of uploaded bundle
  ipfsCid: process.env.IPFS_CID || 'REPLACE_WITH_IPFS_CID',
  
  // Commit tag
  tag: 'LegalShield-v1.0'
};

// CommitRegistry ABI
const abi = parseAbi([
  'function commit(bytes32 b3Hash, string memory ipfsCid, string memory tag)'
]);

async function commitLegalShield() {
  console.log('Creating wallet client for Base L2...');
  
  // Create account from private key
  const account = privateKeyToAccount(CONFIG.privateKey);
  
  // Create wallet client
  const client = createWalletClient({
    chain: CONFIG.chain,
    transport: http(),
    account
  });
  
  console.log(`Wallet address: ${account.address}`);
  console.log(`Chain: ${CONFIG.chain.name}`);
  
  // Format hash as bytes32
  const b3Hash = CONFIG.blake3Hash.startsWith('0x')
    ? CONFIG.blake3Hash
    : `0x${CONFIG.blake3Hash}`;
  
  console.log('\nCommitting to CommitRegistry:');
  console.log(`  Hash: ${b3Hash}`);
  console.log(`  IPFS CID: ${CONFIG.ipfsCid}`);
  console.log(`  Tag: ${CONFIG.tag}`);
  
  // Execute commit transaction
  const hash = await client.writeContract({
    address: CONFIG.contractAddress,
    abi,
    functionName: 'commit',
    args: [b3Hash, CONFIG.ipfsCid, CONFIG.tag]
  });
  
  console.log(`\nTransaction hash: ${hash}`);
  console.log('\nLegal shield committed successfully!');
  
  return hash;
}

// Execute
commitLegalShield().catch((error) => {
  console.error('\nError committing legal shield:', error.message);
  process.exit(1);
});
