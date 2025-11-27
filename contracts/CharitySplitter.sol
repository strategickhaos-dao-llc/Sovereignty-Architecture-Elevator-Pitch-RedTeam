// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title CharitySplitter
 * @notice Automatically splits incoming ETH: 93% to operations, 7% to charity vault
 * @dev Part of SwarmGate v1.0 — Irrevocable 7% Charity Engine
 */
contract CharitySplitter {
    address public immutable opsWallet;
    address public immutable charityVault;

    uint256 public constant CHARITY_BPS = 700; // 7% in basis points
    uint256 public constant BPS_DENOMINATOR = 10000;

    event Split(uint256 total, uint256 toOps, uint256 toCharity);

    constructor(address _opsWallet, address _charityVault) {
        require(_opsWallet != address(0), "Invalid ops wallet");
        require(_charityVault != address(0), "Invalid charity vault");
        opsWallet = _opsWallet;
        charityVault = _charityVault;
    }

    receive() external payable {
        _split(msg.value);
    }

    function _split(uint256 amount) internal {
        uint256 charityAmount = (amount * CHARITY_BPS) / BPS_DENOMINATOR;
        uint256 opsAmount = amount - charityAmount;

        (bool successCharity, ) = charityVault.call{value: charityAmount}("");
        require(successCharity, "Charity transfer failed");

        (bool successOps, ) = opsWallet.call{value: opsAmount}("");
        require(successOps, "Ops transfer failed");

        emit Split(amount, opsAmount, charityAmount);
    }
}
