// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";

/**
 * @title MerkleDistributor
 * @notice Holds the 7% charity allocation and distributes via Merkle proofs
 * @dev Receives ETH from CharitySplitter and allows verified beneficiaries to claim
 */
contract MerkleDistributor {
    bytes32 public immutable merkleRoot;
    mapping(uint256 => bool) public claimed;

    event Claimed(uint256 indexed index, address indexed account, uint256 amount);

    constructor(bytes32 _merkleRoot) {
        merkleRoot = _merkleRoot;
    }

    /**
     * @notice Claim allocated funds using Merkle proof
     * @param index The index of the beneficiary in the Merkle tree
     * @param account The address of the beneficiary
     * @param amount The amount allocated to the beneficiary
     * @param merkleProof The Merkle proof verifying the claim
     */
    function claim(
        uint256 index,
        address account,
        uint256 amount,
        bytes32[] calldata merkleProof
    ) external {
        require(!claimed[index], "Already claimed");

        bytes32 node = keccak256(abi.encodePacked(index, account, amount));
        require(MerkleProof.verify(merkleProof, merkleRoot, node), "Invalid proof");

        claimed[index] = true;

        (bool success, ) = account.call{value: amount}("");
        require(success, "Transfer failed");

        emit Claimed(index, account, amount);
    }

    /**
     * @notice Check if an index has been claimed
     * @param index The index to check
     * @return Whether the index has been claimed
     */
    function isClaimed(uint256 index) external view returns (bool) {
        return claimed[index];
    }

    // Allow contract to receive ETH
    receive() external payable {}
}
