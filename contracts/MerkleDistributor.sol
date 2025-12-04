// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";

/**
 * @title MerkleDistributor
 * @notice Receives 7% of all funds and distributes to verified charities via Merkle proofs
 * @dev Part of SwarmGate v1.0 — Irrevocable 7% Charity Engine
 */
contract MerkleDistributor {
    bytes32 public immutable merkleRoot;
    mapping(uint256 => bool) public claimed;

    event Claimed(uint256 indexed index, address indexed account, uint256 amount);

    constructor(bytes32 _merkleRoot) {
        merkleRoot = _merkleRoot;
    }

    receive() external payable {}

    /**
     * @notice Claim charity allocation using Merkle proof
     * @param index Index of the claim in the Merkle tree
     * @param account Address to receive the funds
     * @param amount Amount to claim
     * @param merkleProof Proof verifying the claim
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
     * @notice Get contract balance
     * @return Current ETH balance of the distributor
     */
    function balance() external view returns (uint256) {
        return address(this).balance;
    }
}
