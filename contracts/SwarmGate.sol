// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title SwarmGate
 * @notice Eternal 7% Revenue Split Engine for Sovereignty Architecture
 * @dev Implements immutable revenue allocation with configurable recipients
 * 
 * Architecture:
 * - Revenue streams send 7% of their earnings to this contract
 * - The contract holds the 7% portion and distributes it among recipients
 * - distribute() splits the contract's entire balance (which represents the 7% allocation)
 * 
 * The distribution ratios are:
 * - 40% → Operations (2.8% of original revenue)
 * - 30% → Development (2.1% of original revenue)
 * - 20% → Governance (1.4% of original revenue)
 * - 10% → Reserves (0.7% of original revenue)
 */
contract SwarmGate {
    // Constants
    // TOTAL_SPLIT_BPS: Used by calculateSplit() to compute 7% of revenue for external callers
    uint256 public constant TOTAL_SPLIT_BPS = 700;      // 7% in basis points
    uint256 public constant BPS_DENOMINATOR = 10000;
    
    // Distribution shares: How the contract's balance (the 7% allocation) is split
    uint256 public constant OPS_SHARE = 40;             // 40% of balance
    uint256 public constant DEV_SHARE = 30;             // 30% of balance
    uint256 public constant GOV_SHARE = 20;             // 20% of balance
    uint256 public constant RESERVE_SHARE = 10;         // 10% of balance
    uint256 public constant SHARE_DENOMINATOR = 100;
    
    // Gas limit for ETH transfers to prevent gas griefing
    uint256 public constant TRANSFER_GAS_LIMIT = 10000;

    // Recipients
    address public immutable operationsRecipient;
    address public immutable developmentRecipient;
    address public immutable governanceRecipient;
    address public immutable reservesRecipient;

    // State
    uint256 public totalDistributed;
    uint256 public distributionCount;
    bool public paused;
    address public immutable admin;

    // Events
    event RevenueReceived(address indexed sender, uint256 amount, uint256 timestamp);
    event SplitDistributed(
        uint256 indexed distributionId,
        uint256 opsAmount,
        uint256 devAmount,
        uint256 govAmount,
        uint256 reserveAmount,
        uint256 timestamp
    );
    event EmergencyPause(address indexed admin, uint256 timestamp);
    event EmergencyUnpause(address indexed admin, uint256 timestamp);

    // Errors
    error ZeroAddress();
    error ContractPaused();
    error NotAdmin();
    error TransferFailed();
    error NoFundsToDistribute();

    modifier onlyAdmin() {
        if (msg.sender != admin) revert NotAdmin();
        _;
    }

    modifier whenNotPaused() {
        if (paused) revert ContractPaused();
        _;
    }

    /**
     * @notice Deploy SwarmGate with recipient addresses
     * @param _ops Operations treasury address
     * @param _dev Development fund address
     * @param _gov Governance address
     * @param _reserves Reserves address
     * @param _admin Admin address for emergency controls
     */
    constructor(
        address _ops,
        address _dev,
        address _gov,
        address _reserves,
        address _admin
    ) {
        if (_ops == address(0) || _dev == address(0) || 
            _gov == address(0) || _reserves == address(0) ||
            _admin == address(0)) {
            revert ZeroAddress();
        }

        operationsRecipient = _ops;
        developmentRecipient = _dev;
        governanceRecipient = _gov;
        reservesRecipient = _reserves;
        admin = _admin;
    }

    /**
     * @notice Receive ETH and emit event
     */
    receive() external payable {
        emit RevenueReceived(msg.sender, msg.value, block.timestamp);
    }

    /**
     * @notice Distribute accumulated funds according to split
     */
    function distribute() external whenNotPaused {
        uint256 balance = address(this).balance;
        if (balance == 0) revert NoFundsToDistribute();

        // Calculate split amounts
        uint256 opsAmount = (balance * OPS_SHARE) / SHARE_DENOMINATOR;
        uint256 devAmount = (balance * DEV_SHARE) / SHARE_DENOMINATOR;
        uint256 govAmount = (balance * GOV_SHARE) / SHARE_DENOMINATOR;
        uint256 reserveAmount = balance - opsAmount - devAmount - govAmount;

        // Transfer to recipients
        _safeTransfer(operationsRecipient, opsAmount);
        _safeTransfer(developmentRecipient, devAmount);
        _safeTransfer(governanceRecipient, govAmount);
        _safeTransfer(reservesRecipient, reserveAmount);

        // Update state
        distributionCount++;
        totalDistributed += balance;

        emit SplitDistributed(
            distributionCount,
            opsAmount,
            devAmount,
            govAmount,
            reserveAmount,
            block.timestamp
        );
    }

    /**
     * @notice Emergency pause distributions
     */
    function pause() external onlyAdmin {
        paused = true;
        emit EmergencyPause(msg.sender, block.timestamp);
    }

    /**
     * @notice Resume distributions after emergency
     */
    function unpause() external onlyAdmin {
        paused = false;
        emit EmergencyUnpause(msg.sender, block.timestamp);
    }

    /**
     * @notice View current balance awaiting distribution
     */
    function pendingDistribution() external view returns (uint256) {
        return address(this).balance;
    }

    /**
     * @notice Calculate the 7% split amounts for a given gross revenue
     * @dev This is a utility function for external callers to preview the split
     *      before sending funds. The returned amounts represent what would be
     *      distributed if 7% of the revenue were sent to this contract.
     * @param revenue The gross revenue amount to calculate the 7% split for
     * @return opsAmount Amount that would go to operations (40% of 7%)
     * @return devAmount Amount that would go to development (30% of 7%)
     * @return govAmount Amount that would go to governance (20% of 7%)
     * @return reserveAmount Amount that would go to reserves (10% of 7%)
     */
    function calculateSplit(uint256 revenue) external pure returns (
        uint256 opsAmount,
        uint256 devAmount,
        uint256 govAmount,
        uint256 reserveAmount
    ) {
        // First calculate 7% of the gross revenue
        uint256 splitAmount = (revenue * TOTAL_SPLIT_BPS) / BPS_DENOMINATOR;
        // Then distribute that 7% among recipients
        opsAmount = (splitAmount * OPS_SHARE) / SHARE_DENOMINATOR;
        devAmount = (splitAmount * DEV_SHARE) / SHARE_DENOMINATOR;
        govAmount = (splitAmount * GOV_SHARE) / SHARE_DENOMINATOR;
        reserveAmount = splitAmount - opsAmount - devAmount - govAmount;
    }

    /**
     * @dev Safe ETH transfer with gas limit to prevent griefing
     */
    function _safeTransfer(address to, uint256 amount) internal {
        (bool success, ) = to.call{value: amount, gas: TRANSFER_GAS_LIMIT}("");
        if (!success) revert TransferFailed();
    }
}
