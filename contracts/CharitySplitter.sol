// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title CharitySplitter
 * @notice Irrevocably splits incoming ETH: 93% to operations wallet, 7% to charity distributor
 * @dev Part of Strategickhaos DAO's sovereign governance infrastructure
 * @custom:security-contact domenic.garza@snhu.edu
 */
contract CharitySplitter is ReentrancyGuard {
    /// @notice Operations wallet receives 93% of all incoming funds
    address public immutable opsWallet;
    
    /// @notice Charity distributor receives 7% of all incoming funds
    address public immutable charityDistributor;
    
    /// @notice Basis points for charity allocation (700 = 7%)
    uint256 public constant CHARITY_BPS = 700;
    
    /// @notice Basis points denominator (10000 = 100%)
    uint256 public constant BPS_DENOMINATOR = 10000;

    /// @notice Emitted when funds are split
    event FundsSplit(
        address indexed sender,
        uint256 totalAmount,
        uint256 opsAmount,
        uint256 charityAmount
    );

    /// @notice Error when transfer fails
    error TransferFailed();
    
    /// @notice Error when zero address is provided
    error ZeroAddress();

    /**
     * @notice Initialize the splitter with immutable wallet addresses
     * @param _opsWallet Address to receive 93% of funds
     * @param _charityDistributor Address to receive 7% of funds
     */
    constructor(address _opsWallet, address _charityDistributor) {
        if (_opsWallet == address(0) || _charityDistributor == address(0)) {
            revert ZeroAddress();
        }
        opsWallet = _opsWallet;
        charityDistributor = _charityDistributor;
    }

    /**
     * @notice Receive and automatically split incoming ETH
     * @dev Reentrancy guard prevents callback attacks
     */
    receive() external payable nonReentrant {
        _split(msg.value);
    }

    /**
     * @notice Fallback for calls with data
     */
    fallback() external payable nonReentrant {
        _split(msg.value);
    }

    /**
     * @notice Internal function to split funds
     * @param amount Total amount to split
     */
    function _split(uint256 amount) internal {
        uint256 charityAmount = (amount * CHARITY_BPS) / BPS_DENOMINATOR;
        uint256 opsAmount = amount - charityAmount;

        // Transfer to operations wallet
        (bool opsSuccess, ) = opsWallet.call{value: opsAmount}("");
        if (!opsSuccess) revert TransferFailed();

        // Transfer to charity distributor
        (bool charitySuccess, ) = charityDistributor.call{value: charityAmount}("");
        if (!charitySuccess) revert TransferFailed();

        emit FundsSplit(msg.sender, amount, opsAmount, charityAmount);
    }

    /**
     * @notice Get the split amounts for a given input
     * @param amount Input amount to calculate split
     * @return opsAmount Amount that would go to operations
     * @return charityAmount Amount that would go to charity
     */
    function calculateSplit(uint256 amount) external pure returns (uint256 opsAmount, uint256 charityAmount) {
        charityAmount = (amount * CHARITY_BPS) / BPS_DENOMINATOR;
        opsAmount = amount - charityAmount;
    }
}
