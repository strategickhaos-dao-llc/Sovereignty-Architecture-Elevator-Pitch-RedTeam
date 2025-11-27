// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title MerkleDistributor
 * @dev Distributes ETH to beneficiaries using Merkle proofs for efficiency
 * @notice Part of SwarmGate v1.0 - Perpetual Philanthropy Engine
 * @author Strategickhaos DAO LLC / ValorYield Engine
 * 
 * This contract enables efficient batch distribution to multiple charity
 * beneficiaries using Merkle tree verification.
 */
contract MerkleDistributor is Ownable, ReentrancyGuard {
    // Merkle root for current distribution round
    bytes32 public merkleRoot;
    
    // Distribution round tracking
    uint256 public currentRound;
    
    // Mapping: round => account => claimed
    mapping(uint256 => mapping(address => bool)) public claimed;
    
    // Mapping: round => account => amount claimed
    mapping(uint256 => mapping(address => uint256)) public claimedAmount;
    
    // Total distributed per round
    mapping(uint256 => uint256) public roundTotalDistributed;
    
    // Global tracking
    uint256 public totalDistributed;

    // Events
    event MerkleRootUpdated(uint256 indexed round, bytes32 newRoot);
    event Claimed(uint256 indexed round, address indexed account, uint256 amount);
    event RoundAdvanced(uint256 indexed oldRound, uint256 indexed newRound);
    event FundsDeposited(address indexed depositor, uint256 amount);

    /**
     * @dev Constructor initializes with empty merkle root
     */
    constructor() Ownable(msg.sender) {
        currentRound = 1;
    }

    /**
     * @dev Receive ETH deposits
     */
    receive() external payable {
        emit FundsDeposited(msg.sender, msg.value);
    }

    /**
     * @dev Set a new Merkle root for the current round
     * @param _merkleRoot New Merkle root
     */
    function setMerkleRoot(bytes32 _merkleRoot) external onlyOwner {
        require(_merkleRoot != bytes32(0), "MerkleDistributor: invalid merkle root");
        merkleRoot = _merkleRoot;
        emit MerkleRootUpdated(currentRound, _merkleRoot);
    }

    /**
     * @dev Advance to a new distribution round with a new Merkle root
     * @param _newMerkleRoot Merkle root for the new round
     */
    function advanceRound(bytes32 _newMerkleRoot) external onlyOwner {
        require(_newMerkleRoot != bytes32(0), "MerkleDistributor: invalid merkle root");
        
        uint256 oldRound = currentRound;
        currentRound++;
        merkleRoot = _newMerkleRoot;
        
        emit RoundAdvanced(oldRound, currentRound);
        emit MerkleRootUpdated(currentRound, _newMerkleRoot);
    }

    /**
     * @dev Claim distribution for the current round
     * @param amount Amount to claim
     * @param merkleProof Merkle proof for verification
     */
    function claim(
        uint256 amount,
        bytes32[] calldata merkleProof
    ) external nonReentrant {
        require(!claimed[currentRound][msg.sender], "MerkleDistributor: already claimed");
        require(amount > 0, "MerkleDistributor: amount is zero");
        require(address(this).balance >= amount, "MerkleDistributor: insufficient balance");

        // Verify the merkle proof
        bytes32 leaf = keccak256(bytes.concat(keccak256(abi.encode(msg.sender, amount))));
        require(
            MerkleProof.verify(merkleProof, merkleRoot, leaf),
            "MerkleDistributor: invalid proof"
        );

        // Mark as claimed
        claimed[currentRound][msg.sender] = true;
        claimedAmount[currentRound][msg.sender] = amount;
        roundTotalDistributed[currentRound] += amount;
        totalDistributed += amount;

        // Transfer funds
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "MerkleDistributor: transfer failed");

        emit Claimed(currentRound, msg.sender, amount);
    }

    /**
     * @dev Check if an address has claimed in a specific round
     * @param round Round number to check
     * @param account Address to check
     */
    function hasClaimed(uint256 round, address account) external view returns (bool) {
        return claimed[round][account];
    }

    /**
     * @dev Verify a merkle proof without claiming
     * @param account Address to verify
     * @param amount Amount in the claim
     * @param merkleProof Merkle proof
     */
    function verifyProof(
        address account,
        uint256 amount,
        bytes32[] calldata merkleProof
    ) external view returns (bool) {
        bytes32 leaf = keccak256(bytes.concat(keccak256(abi.encode(account, amount))));
        return MerkleProof.verify(merkleProof, merkleRoot, leaf);
    }

    /**
     * @dev Get contract balance
     */
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }

    /**
     * @dev Get distribution statistics
     * @return _currentRound Current distribution round
     * @return _totalDistributed Total ETH distributed all time
     * @return _currentRoundDistributed Total distributed in current round
     * @return _balance Current contract balance
     */
    function getStats() external view returns (
        uint256 _currentRound,
        uint256 _totalDistributed,
        uint256 _currentRoundDistributed,
        uint256 _balance
    ) {
        return (
            currentRound,
            totalDistributed,
            roundTotalDistributed[currentRound],
            address(this).balance
        );
    }

    /**
     * @dev Emergency withdraw any stuck funds (only owner)
     * @notice This should only be used in emergency situations
     * @param to Address to send stuck funds
     */
    function emergencyWithdraw(address to) external onlyOwner {
        require(to != address(0), "MerkleDistributor: withdraw to zero address");
        uint256 balance = address(this).balance;
        require(balance > 0, "MerkleDistributor: no balance");
        
        (bool success, ) = to.call{value: balance}("");
        require(success, "MerkleDistributor: withdraw failed");
    }
}
