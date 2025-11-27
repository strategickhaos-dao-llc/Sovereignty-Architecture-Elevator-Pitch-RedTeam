// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title MerkleDistributor
 * @notice Distributes charity funds to named charities using Merkle proofs.
 * @dev Each charity is verified via Merkle proof for trustless verification.
 *      The Merkle root is immutable after deployment - charities are fixed forever.
 *      
 * Named charities (example configuration):
 * - St. Jude Children's Research Hospital
 * - Doctors Without Borders
 * - Electronic Frontier Foundation
 * - Direct Relief
 * - charity: water
 * - World Wildlife Fund
 * - Feeding America
 * 
 * Each charity has an equal share of the 7% allocation.
 */
contract MerkleDistributor is ReentrancyGuard {
    /// @notice Immutable Merkle root for charity verification
    bytes32 public immutable merkleRoot;
    
    /// @notice Total ETH received for distribution
    uint256 public totalReceived;
    
    /// @notice Total ETH claimed by charities
    uint256 public totalClaimed;
    
    /// @notice Mapping to track claimed amounts per charity
    mapping(address => uint256) public claimedAmounts;
    
    /// @notice Mapping to track allocated amounts per charity index
    mapping(uint256 => uint256) public allocatedAmounts;
    
    /// @notice Event emitted when a charity claims their allocation
    event CharityClaimed(
        uint256 indexed charityIndex,
        address indexed charity,
        uint256 amount,
        uint256 timestamp
    );
    
    /// @notice Event emitted when funds are received
    event FundsReceived(address indexed sender, uint256 amount, uint256 timestamp);
    
    /// @notice Distribution epoch for tracking
    uint256 public currentEpoch;
    
    /// @notice Epoch allocations
    mapping(uint256 => uint256) public epochAllocations;
    
    /// @notice Claimed in epoch by charity
    mapping(uint256 => mapping(uint256 => bool)) public claimedInEpoch;

    /// @notice Number of charities in the Merkle tree
    uint256 public immutable charityCount;

    /**
     * @notice Constructor sets the immutable Merkle root
     * @param _merkleRoot The Merkle root of all charity addresses and allocations
     * @param _charityCount Number of charities in the distribution
     */
    constructor(bytes32 _merkleRoot, uint256 _charityCount) {
        require(_merkleRoot != bytes32(0), "Invalid merkle root");
        require(_charityCount > 0, "Must have at least one charity");
        
        merkleRoot = _merkleRoot;
        charityCount = _charityCount;
    }
    
    /**
     * @notice Receive ETH from CharitySplitter
     */
    receive() external payable {
        totalReceived += msg.value;
        currentEpoch++;
        epochAllocations[currentEpoch] = msg.value;
        emit FundsReceived(msg.sender, msg.value, block.timestamp);
    }
    
    /**
     * @notice Claim charity allocation with Merkle proof
     * @param charityIndex Index of the charity in the Merkle tree
     * @param charity Address of the charity
     * @param merkleProof Merkle proof for verification
     */
    function claim(
        uint256 charityIndex,
        address payable charity,
        bytes32[] calldata merkleProof
    ) external nonReentrant {
        require(!claimedInEpoch[currentEpoch][charityIndex], "Already claimed in epoch");
        require(currentEpoch > 0, "No funds to claim");
        
        // Verify the Merkle proof
        bytes32 leaf = keccak256(bytes.concat(keccak256(abi.encode(charityIndex, charity))));
        require(MerkleProof.verify(merkleProof, merkleRoot, leaf), "Invalid proof");
        
        // Calculate share (equal distribution among all charities)
        uint256 epochAmount = epochAllocations[currentEpoch];
        uint256 share = epochAmount / charityCount;
        
        require(share > 0, "No funds available");
        
        claimedInEpoch[currentEpoch][charityIndex] = true;
        claimedAmounts[charity] += share;
        allocatedAmounts[charityIndex] += share;
        totalClaimed += share;
        
        emit CharityClaimed(charityIndex, charity, share, block.timestamp);
        
        // Transfer the share
        (bool success, ) = charity.call{value: share}("");
        require(success, "Transfer failed");
    }
    
    /**
     * @notice Get claimable amount for a charity in current epoch
     * @param charityIndex Index of the charity
     * @return amount Claimable amount
     */
    function getClaimable(uint256 charityIndex) external view returns (uint256 amount) {
        if (currentEpoch == 0) return 0;
        if (claimedInEpoch[currentEpoch][charityIndex]) return 0;
        
        return epochAllocations[currentEpoch] / charityCount;
    }
    
    /**
     * @notice Get statistics
     * @return received Total received
     * @return claimed Total claimed
     * @return pending Pending distribution
     * @return epoch Current epoch
     */
    function getStats() external view returns (
        uint256 received,
        uint256 claimed,
        uint256 pending,
        uint256 epoch
    ) {
        return (totalReceived, totalClaimed, address(this).balance, currentEpoch);
    }
    
    /**
     * @notice Verify if an address is a valid charity
     * @param charityIndex Index of the charity
     * @param charity Address to verify
     * @param merkleProof Merkle proof
     * @return valid True if the proof is valid
     */
    function verifyCharity(
        uint256 charityIndex,
        address charity,
        bytes32[] calldata merkleProof
    ) external view returns (bool valid) {
        bytes32 leaf = keccak256(bytes.concat(keccak256(abi.encode(charityIndex, charity))));
        return MerkleProof.verify(merkleProof, merkleRoot, leaf);
    }
}
