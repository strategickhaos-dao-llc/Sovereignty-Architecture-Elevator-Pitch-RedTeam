// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";

/**
 * @title MerkleDistributor
 * @notice Distributes ETH to charity beneficiaries using Merkle proofs
 * @dev Charity addresses and allocations are encoded in the Merkle tree
 */
contract MerkleDistributor {
    bytes32 public immutable merkleRoot;

    mapping(address => bool) public hasClaimed;

    event Claimed(address indexed beneficiary, uint256 amount);
    event FundsReceived(address indexed sender, uint256 amount);

    constructor(bytes32 _merkleRoot) {
        merkleRoot = _merkleRoot;
    }

    receive() external payable {
        emit FundsReceived(msg.sender, msg.value);
    }

    fallback() external payable {
        emit FundsReceived(msg.sender, msg.value);
    }

    /**
     * @notice Claim ETH allocation as a beneficiary
     * @param amount The amount to claim
     * @param merkleProof The Merkle proof for the claim
     */
    function claim(uint256 amount, bytes32[] calldata merkleProof) external {
        require(!hasClaimed[msg.sender], "Already claimed");

        bytes32 leaf = keccak256(abi.encodePacked(msg.sender, amount));
        require(MerkleProof.verify(merkleProof, merkleRoot, leaf), "Invalid proof");

        hasClaimed[msg.sender] = true;

        (bool sent, ) = payable(msg.sender).call{value: amount}("");
        require(sent, "Transfer failed");

        emit Claimed(msg.sender, amount);
    }

    /**
     * @notice Get the contract's ETH balance
     */
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
