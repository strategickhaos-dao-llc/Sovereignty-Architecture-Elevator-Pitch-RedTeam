// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title CharitySplitter
 * @notice Splits incoming ETH 93% to operations, 7% to charity distributor
 * @dev The 7% allocation is immutable and enforced on-chain
 */
contract CharitySplitter {
    address payable public immutable opsWallet;
    address payable public immutable charityDistributor;

    uint256 public constant OPS_BPS = 9300;    // 93%
    uint256 public constant CHARITY_BPS = 700; // 7%
    uint256 public constant BPS_DENOMINATOR = 10000;

    event Split(uint256 total, uint256 toOps, uint256 toCharity);

    constructor(address _opsWallet, address _charityDistributor) {
        require(_opsWallet != address(0), "Invalid ops wallet");
        require(_charityDistributor != address(0), "Invalid charity distributor");
        opsWallet = payable(_opsWallet);
        charityDistributor = payable(_charityDistributor);
    }

    receive() external payable {
        _split(msg.value);
    }

    fallback() external payable {
        _split(msg.value);
    }

    function _split(uint256 amount) internal {
        require(amount > 0, "No ETH sent");

        uint256 charityAmount = (amount * CHARITY_BPS) / BPS_DENOMINATOR;
        uint256 opsAmount = amount - charityAmount;

        (bool sentOps, ) = opsWallet.call{value: opsAmount}("");
        require(sentOps, "Ops transfer failed");

        (bool sentCharity, ) = charityDistributor.call{value: charityAmount}("");
        require(sentCharity, "Charity transfer failed");

        emit Split(amount, opsAmount, charityAmount);
    }
}
