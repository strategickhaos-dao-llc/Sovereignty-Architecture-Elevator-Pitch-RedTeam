// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title MerkleDistributor
 * @notice Holds funds for charities and allows claiming via Merkle Proofs.
 */
contract MerkleDistributor is ReentrancyGuard {
    bytes32 public immutable merkleRoot;
    
    // Mapping to track claimed amounts per index to prevent double claiming per epoch/drop
    // For a continuous stream, a more complex drip mechanism would be used.
    // This implementation assumes periodic "drops" or a one-time setup for the MVP.
    mapping(uint256 => uint256) private _claimedBitMap;

    event Claimed(uint256 index, address account, uint256 amount);
    event Received(address sender, uint256 amount);

    constructor(bytes32 _merkleRoot) {
        merkleRoot = _merkleRoot;
    }

    receive() external payable {
        emit Received(msg.sender, msg.value);
    }

    function isClaimed(uint256 index) public view returns (bool) {
        uint256 claimedWordIndex = index / 256;
        uint256 claimedBitIndex = index % 256;
        uint256 claimedWord = _claimedBitMap[claimedWordIndex];
        uint256 mask = (1 << claimedBitIndex);
        return claimedWord & mask == mask;
    }

    function _setClaimed(uint256 index) private {
        uint256 claimedWordIndex = index / 256;
        uint256 claimedBitIndex = index % 256;
        _claimedBitMap[claimedWordIndex] = _claimedBitMap[claimedWordIndex] | (1 << claimedBitIndex);
    }

    function claim(
        uint256 index,
        address payable account,
        uint256 amount,
        bytes32[] calldata merkleProof
    ) external nonReentrant {
        require(!isClaimed(index), "MerkleDistributor: Drop already claimed");

        // Verify the merkle proof
        bytes32 node = keccak256(abi.encodePacked(index, account, amount));
        require(
            MerkleProof.verify(merkleProof, merkleRoot, node),
            "MerkleDistributor: Invalid proof"
        );

        // Mark it claimed and send the token
        _setClaimed(index);
        
        (bool success, ) = account.call{value: amount}("");
        require(success, "MerkleDistributor: Transfer failed");

        emit Claimed(index, account, amount);
    }
}
