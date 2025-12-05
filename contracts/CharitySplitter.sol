// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title CharitySplitter
 * @notice Splits incoming ETH 93% to operations, 7% to charity distributor
 * @dev SwarmGate v1.0 Engine - mathematically enforced 93/7 split
 *
 * The 7% is no longer a promise, it's physics.
 */
contract CharitySplitter {
    address public immutable opsWallet;
    address public immutable charityDistributor;

    uint256 public constant OPS_SHARE = 93;
    uint256 public constant CHARITY_SHARE = 7;
    uint256 public constant TOTAL_SHARE = 100;

    uint256 public totalReceived;
    uint256 public totalToOps;
    uint256 public totalToCharity;

    event Split(
        address indexed sender,
        uint256 amount,
        uint256 toOps,
        uint256 toCharity
    );

    constructor(address _opsWallet, address _charityDistributor) {
        require(_opsWallet != address(0), "Invalid ops wallet");
        require(_charityDistributor != address(0), "Invalid charity distributor");
        opsWallet = _opsWallet;
        charityDistributor = _charityDistributor;
    }

    /**
     * @notice Receive ETH and automatically split 93/7
     */
    receive() external payable {
        _split(msg.value);
    }

    /**
     * @notice Fallback function to handle any incoming ETH
     */
    fallback() external payable {
        _split(msg.value);
    }

    function _split(uint256 amount) internal {
        require(amount > 0, "Amount must be greater than 0");

        uint256 toOps = (amount * OPS_SHARE) / TOTAL_SHARE;
        uint256 toCharity = amount - toOps; // Ensures no dust is lost

        totalReceived += amount;
        totalToOps += toOps;
        totalToCharity += toCharity;

        // Transfer to operations wallet
        (bool opsSuccess, ) = opsWallet.call{value: toOps}("");
        require(opsSuccess, "Ops transfer failed");

        // Transfer to charity distributor
        (bool charitySuccess, ) = charityDistributor.call{value: toCharity}("");
        require(charitySuccess, "Charity transfer failed");

        emit Split(msg.sender, amount, toOps, toCharity);
    }

    /**
     * @notice Get split amounts for a given input
     * @param amount The amount to calculate split for
     * @return toOps Amount going to operations (93%)
     * @return toCharity Amount going to charity (7%)
     */
    function calculateSplit(uint256 amount) external pure returns (uint256 toOps, uint256 toCharity) {
        toOps = (amount * OPS_SHARE) / TOTAL_SHARE;
        toCharity = amount - toOps;
    }
}
