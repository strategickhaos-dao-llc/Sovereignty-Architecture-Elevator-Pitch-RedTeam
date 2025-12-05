// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title CharitySplitter
 * @dev Automatically splits incoming ETH: 7% to charity pool, 93% to treasury
 * @notice Part of SwarmGate v1.0 - Perpetual Philanthropy Engine
 * @author Strategickhaos DAO LLC / ValorYield Engine
 * 
 * The 7% allocation is IRREVOCABLE by design - this contract enforces the
 * promise that 7% of all inflows will always go to charitable causes.
 */
contract CharitySplitter is Ownable, ReentrancyGuard {
    // Charity allocation percentage (7% = 700 basis points)
    uint256 public constant CHARITY_BPS = 700;
    uint256 public constant BPS_DENOMINATOR = 10000;

    // Addresses for fund allocation
    address public charityPool;
    address public treasury;

    // Tracking
    uint256 public totalReceived;
    uint256 public totalToCharity;
    uint256 public totalToTreasury;

    // Events
    event FundsReceived(address indexed sender, uint256 amount);
    event FundsSplit(uint256 charityAmount, uint256 treasuryAmount);
    event CharityPoolUpdated(address indexed oldPool, address indexed newPool);
    event TreasuryUpdated(address indexed oldTreasury, address indexed newTreasury);
    event EmergencyWithdraw(address indexed to, uint256 amount);

    /**
     * @dev Constructor sets initial charity pool and treasury addresses
     * @param _charityPool Address where charity funds are sent
     * @param _treasury Address where treasury funds are sent
     */
    constructor(address _charityPool, address _treasury) Ownable(msg.sender) {
        require(_charityPool != address(0), "CharitySplitter: charity pool is zero address");
        require(_treasury != address(0), "CharitySplitter: treasury is zero address");
        
        charityPool = _charityPool;
        treasury = _treasury;
    }

    /**
     * @dev Receive function - automatically splits incoming ETH
     */
    receive() external payable nonReentrant {
        _splitFunds(msg.value);
    }

    /**
     * @dev Fallback function for any call with data
     */
    fallback() external payable nonReentrant {
        _splitFunds(msg.value);
    }

    /**
     * @dev Internal function to split funds according to 7/93 ratio
     * @param amount The amount of ETH to split
     */
    function _splitFunds(uint256 amount) internal {
        require(amount > 0, "CharitySplitter: amount is zero");

        uint256 charityAmount = (amount * CHARITY_BPS) / BPS_DENOMINATOR;
        uint256 treasuryAmount = amount - charityAmount;

        // Update tracking
        totalReceived += amount;
        totalToCharity += charityAmount;
        totalToTreasury += treasuryAmount;

        emit FundsReceived(msg.sender, amount);

        // Transfer to charity pool
        (bool charitySuccess, ) = charityPool.call{value: charityAmount}("");
        require(charitySuccess, "CharitySplitter: charity transfer failed");

        // Transfer to treasury
        (bool treasurySuccess, ) = treasury.call{value: treasuryAmount}("");
        require(treasurySuccess, "CharitySplitter: treasury transfer failed");

        emit FundsSplit(charityAmount, treasuryAmount);
    }

    /**
     * @dev Update charity pool address (only owner)
     * @param _newCharityPool New charity pool address
     */
    function setCharityPool(address _newCharityPool) external onlyOwner {
        require(_newCharityPool != address(0), "CharitySplitter: new charity pool is zero address");
        address oldPool = charityPool;
        charityPool = _newCharityPool;
        emit CharityPoolUpdated(oldPool, _newCharityPool);
    }

    /**
     * @dev Update treasury address (only owner)
     * @param _newTreasury New treasury address
     */
    function setTreasury(address _newTreasury) external onlyOwner {
        require(_newTreasury != address(0), "CharitySplitter: new treasury is zero address");
        address oldTreasury = treasury;
        treasury = _newTreasury;
        emit TreasuryUpdated(oldTreasury, _newTreasury);
    }

    /**
     * @dev Get current allocation statistics
     * @return _totalReceived Total ETH received by contract
     * @return _totalToCharity Total ETH sent to charity (7%)
     * @return _totalToTreasury Total ETH sent to treasury (93%)
     */
    function getStats() external view returns (
        uint256 _totalReceived,
        uint256 _totalToCharity,
        uint256 _totalToTreasury
    ) {
        return (totalReceived, totalToCharity, totalToTreasury);
    }

    /**
     * @dev Emergency withdraw any stuck funds (only owner)
     * @notice This should only be used if funds get stuck due to failed transfers
     * @param to Address to send stuck funds
     */
    function emergencyWithdraw(address to) external onlyOwner {
        require(to != address(0), "CharitySplitter: withdraw to zero address");
        uint256 balance = address(this).balance;
        require(balance > 0, "CharitySplitter: no balance to withdraw");
        
        (bool success, ) = to.call{value: balance}("");
        require(success, "CharitySplitter: emergency withdraw failed");
        
        emit EmergencyWithdraw(to, balance);
    }
}
