// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title MerkleDistributor
 * @notice Receives and distributes charity funds based on a Merkle tree of recipients
 * @dev Part of the SwarmGate v1.0 Engine - receives 7% of all incoming funds
 */
contract MerkleDistributor {
    bytes32 public merkleRoot;
    mapping(uint256 => uint256) private claimedBitMap;

    event Claimed(uint256 indexed index, address indexed account, uint256 amount);

    constructor(bytes32 _merkleRoot) {
        merkleRoot = _merkleRoot;
    }

    /**
     * @notice Check if an index has already been claimed
     */
    function isClaimed(uint256 index) public view returns (bool) {
        uint256 claimedWordIndex = index / 256;
        uint256 claimedBitIndex = index % 256;
        uint256 claimedWord = claimedBitMap[claimedWordIndex];
        uint256 mask = (1 << claimedBitIndex);
        return claimedWord & mask == mask;
    }

    function _setClaimed(uint256 index) private {
        uint256 claimedWordIndex = index / 256;
        uint256 claimedBitIndex = index % 256;
        claimedBitMap[claimedWordIndex] = claimedBitMap[claimedWordIndex] | (1 << claimedBitIndex);
    }

    /**
     * @notice Claim funds from the distributor
     * @param index The index in the Merkle tree
     * @param account The recipient address
     * @param amount The amount to claim
     * @param merkleProof The Merkle proof
     */
    function claim(
        uint256 index,
        address account,
        uint256 amount,
        bytes32[] calldata merkleProof
    ) external {
        require(!isClaimed(index), "MerkleDistributor: Drop already claimed.");

        bytes32 node = keccak256(abi.encodePacked(index, account, amount));
        require(_verify(merkleProof, node), "MerkleDistributor: Invalid proof.");

        _setClaimed(index);

        (bool success, ) = account.call{value: amount}("");
        require(success, "MerkleDistributor: Transfer failed.");

        emit Claimed(index, account, amount);
    }

    function _verify(bytes32[] calldata proof, bytes32 leaf) internal view returns (bool) {
        bytes32 computedHash = leaf;

        for (uint256 i = 0; i < proof.length; i++) {
            bytes32 proofElement = proof[i];
            if (computedHash <= proofElement) {
                computedHash = keccak256(abi.encodePacked(computedHash, proofElement));
            } else {
                computedHash = keccak256(abi.encodePacked(proofElement, computedHash));
            }
        }

        return computedHash == merkleRoot;
    }

    /**
     * @notice Receive ETH - this is where the 7% charity portion lands
     */
    receive() external payable {}

    /**
     * @notice Get the contract balance
     */
    function balance() external view returns (uint256) {
        return address(this).balance;
    }
}
