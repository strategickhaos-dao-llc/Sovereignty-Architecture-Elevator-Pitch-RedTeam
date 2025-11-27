// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title MerkleDistributor
 * @notice Distributes charity funds to verified recipients using Merkle proofs
 * @dev Recipients can claim their allocation by providing a valid Merkle proof
 * @custom:security-contact domenic.garza@snhu.edu
 */
contract MerkleDistributor is ReentrancyGuard, Ownable {
    /// @notice Merkle root for verifying claims
    bytes32 public merkleRoot;

    /// @notice Bitmap of claimed indices to prevent double-claims
    mapping(uint256 => uint256) private claimedBitMap;

    /// @notice Emitted when a successful claim is made
    event Claimed(uint256 indexed index, address indexed account, uint256 amount);

    /// @notice Emitted when the merkle root is updated
    event MerkleRootUpdated(bytes32 indexed oldRoot, bytes32 indexed newRoot);

    /// @notice Error when claim has already been made
    error AlreadyClaimed();

    /// @notice Error when proof is invalid
    error InvalidProof();

    /// @notice Error when transfer fails
    error TransferFailed();

    /// @notice Error when zero root is provided
    error ZeroRoot();

    /**
     * @notice Initialize distributor with a merkle root
     * @param _merkleRoot Root of the merkle tree for claim verification
     */
    constructor(bytes32 _merkleRoot) Ownable(msg.sender) {
        if (_merkleRoot == bytes32(0)) revert ZeroRoot();
        merkleRoot = _merkleRoot;
    }

    /**
     * @notice Receive ETH from the CharitySplitter
     */
    receive() external payable {}

    /**
     * @notice Check if an index has been claimed
     * @param index The index to check
     * @return True if the index has been claimed
     */
    function isClaimed(uint256 index) public view returns (bool) {
        uint256 claimedWordIndex = index / 256;
        uint256 claimedBitIndex = index % 256;
        uint256 claimedWord = claimedBitMap[claimedWordIndex];
        uint256 mask = (1 << claimedBitIndex);
        return claimedWord & mask == mask;
    }

    /**
     * @notice Mark an index as claimed in the bitmap
     * @param index The index to mark as claimed
     */
    function _setClaimed(uint256 index) private {
        uint256 claimedWordIndex = index / 256;
        uint256 claimedBitIndex = index % 256;
        claimedBitMap[claimedWordIndex] = claimedBitMap[claimedWordIndex] | (1 << claimedBitIndex);
    }

    /**
     * @notice Claim allocated funds using a Merkle proof
     * @param index Unique index for this claim
     * @param account Address to receive the funds
     * @param amount Amount to claim
     * @param merkleProof Array of proof elements
     */
    function claim(
        uint256 index,
        address account,
        uint256 amount,
        bytes32[] calldata merkleProof
    ) external nonReentrant {
        if (isClaimed(index)) revert AlreadyClaimed();

        // Verify the merkle proof
        bytes32 node = keccak256(abi.encodePacked(index, account, amount));
        if (!MerkleProof.verify(merkleProof, merkleRoot, node)) {
            revert InvalidProof();
        }

        // Mark as claimed before transfer to prevent reentrancy
        _setClaimed(index);

        // Transfer funds
        (bool success, ) = account.call{value: amount}("");
        if (!success) revert TransferFailed();

        emit Claimed(index, account, amount);
    }

    /**
     * @notice Update the merkle root for a new distribution round
     * @dev Only callable by owner (DAO governance)
     * @param _newMerkleRoot New merkle root for the next distribution
     */
    function updateMerkleRoot(bytes32 _newMerkleRoot) external onlyOwner {
        if (_newMerkleRoot == bytes32(0)) revert ZeroRoot();
        bytes32 oldRoot = merkleRoot;
        merkleRoot = _newMerkleRoot;
        emit MerkleRootUpdated(oldRoot, _newMerkleRoot);
    }

    /**
     * @notice Get the contract's ETH balance
     * @return Current balance available for distribution
     */
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
