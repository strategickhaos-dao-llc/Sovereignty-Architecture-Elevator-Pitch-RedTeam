// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title CharitySplitter
 * @notice Irrevocable payment splitter that allocates 7% to charity forever.
 * @dev This contract splits all incoming ETH: 93% to operations multisig, 7% to charity distributor.
 *      The charity percentage and addresses are immutable after deployment - no rug pulls possible.
 *      
 * Key guarantees:
 * - IMMUTABLE: Charity percentage (7%) cannot be changed after deployment
 * - IMMUTABLE: Operations and charity addresses cannot be changed
 * - APPEND-ONLY: All distributions are logged and verifiable on-chain
 * - TRUSTLESS: No admin keys, no governance capture possible
 * - UNSTOPPABLE: No pause functionality - distributions cannot be halted
 */
contract CharitySplitter is ReentrancyGuard {
    /// @notice Charity allocation in basis points (700 = 7%)
    uint256 public constant CHARITY_BPS = 700;
    
    /// @notice Total basis points (10000 = 100%)
    uint256 public constant TOTAL_BPS = 10000;

    /// @notice Immutable operations multisig address
    address payable public immutable opsMultisig;
    
    /// @notice Immutable charity distributor address (MerkleDistributor contract)
    address payable public immutable charityDistributor;
    
    /// @notice Total ETH received by this contract (running total)
    uint256 public totalReceived;
    
    /// @notice Total ETH sent to operations
    uint256 public totalToOps;
    
    /// @notice Total ETH sent to charity (the "7% forever" counter)
    uint256 public totalToCharity;
    
    /// @notice Distribution event for transparency
    event Distribution(
        uint256 indexed distributionId,
        uint256 amount,
        uint256 toOps,
        uint256 toCharity,
        uint256 timestamp
    );
    
    /// @notice Received ETH event
    event Received(address indexed sender, uint256 amount, uint256 timestamp);
    
    /// @notice Distribution counter for unique IDs
    uint256 public distributionCount;

    /**
     * @notice Constructor sets immutable addresses - no changes possible after deployment
     * @param _opsMultisig Address of operations multisig (receives 93%)
     * @param _charityDistributor Address of charity MerkleDistributor (receives 7%)
     */
    constructor(address payable _opsMultisig, address payable _charityDistributor) {
        require(_opsMultisig != address(0), "Invalid ops address");
        require(_charityDistributor != address(0), "Invalid charity address");
        require(_opsMultisig != _charityDistributor, "Addresses must be different");
        
        opsMultisig = _opsMultisig;
        charityDistributor = _charityDistributor;
    }
    
    /**
     * @notice Receive ETH and automatically split
     */
    receive() external payable {
        emit Received(msg.sender, msg.value, block.timestamp);
        totalReceived += msg.value;
        _distribute();
    }
    
    /**
     * @notice Fallback to receive ETH
     */
    fallback() external payable {
        emit Received(msg.sender, msg.value, block.timestamp);
        totalReceived += msg.value;
        _distribute();
    }
    
    /**
     * @notice Manual distribution trigger (for gas optimization in some cases)
     * @dev Anyone can call this to force distribution of accumulated balance
     */
    function distribute() external nonReentrant {
        _distribute();
    }
    
    /**
     * @notice Internal distribution logic
     * @dev Splits current balance: 93% to ops, 7% to charity
     */
    function _distribute() internal {
        uint256 balance = address(this).balance;
        if (balance == 0) return;
        
        uint256 charityAmount = (balance * CHARITY_BPS) / TOTAL_BPS;
        uint256 opsAmount = balance - charityAmount; // Remaining goes to ops (avoids rounding issues)
        
        distributionCount++;
        totalToOps += opsAmount;
        totalToCharity += charityAmount;
        
        emit Distribution(distributionCount, balance, opsAmount, charityAmount, block.timestamp);
        
        // Transfer to charity first (priority)
        if (charityAmount > 0) {
            (bool charitySuccess, ) = charityDistributor.call{value: charityAmount}("");
            require(charitySuccess, "Charity transfer failed");
        }
        
        // Transfer to operations
        if (opsAmount > 0) {
            (bool opsSuccess, ) = opsMultisig.call{value: opsAmount}("");
            require(opsSuccess, "Ops transfer failed");
        }
    }
    
    /**
     * @notice Get current charity percentage (always 7%)
     * @return percentage The charity percentage (7)
     */
    function getCharityPercentage() external pure returns (uint256 percentage) {
        return CHARITY_BPS / 100;
    }
    
    /**
     * @notice Get contract statistics
     * @return received Total ETH received
     * @return toOps Total ETH sent to operations
     * @return toCharity Total ETH sent to charity ("7% forever" counter)
     * @return distributions Number of distributions
     */
    function getStats() external view returns (
        uint256 received,
        uint256 toOps,
        uint256 toCharity,
        uint256 distributions
    ) {
        return (totalReceived, totalToOps, totalToCharity, distributionCount);
    }
}
