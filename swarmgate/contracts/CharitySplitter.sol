// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title CharitySplitter
 * @notice Splits incoming ETH: 93% to ops wallet, 7% to charity distributor
 * @dev This is the "eternal 7% engine" - the split is mathematically irrevocable
 */
contract CharitySplitter {
    address public immutable opsWallet;
    address public immutable charityDistributor;

    uint256 public constant OPS_SHARE = 93;
    uint256 public constant CHARITY_SHARE = 7;
    uint256 public constant TOTAL_SHARES = 100;

    event Split(uint256 total, uint256 toOps, uint256 toCharity);

    constructor(address _opsWallet, address _charityDistributor) {
        require(_opsWallet != address(0), "Invalid ops wallet");
        require(_charityDistributor != address(0), "Invalid charity distributor");
        opsWallet = _opsWallet;
        charityDistributor = _charityDistributor;
    }

    /**
     * @notice Receives ETH and splits it 93/7
     * @dev The split is mathematically precise and irrevocable
     */
    receive() external payable {
        require(msg.value > 0, "No ETH sent");

        uint256 toCharity = (msg.value * CHARITY_SHARE) / TOTAL_SHARES;
        uint256 toOps = msg.value - toCharity;

        (bool opsSuccess, ) = opsWallet.call{value: toOps}("");
        require(opsSuccess, "Ops transfer failed");

        (bool charitySuccess, ) = charityDistributor.call{value: toCharity}("");
        require(charitySuccess, "Charity transfer failed");

        emit Split(msg.value, toOps, toCharity);
    }
}
