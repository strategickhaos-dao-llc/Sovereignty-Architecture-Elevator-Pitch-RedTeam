// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title SwarmGate
 * @notice Eternal 7% Revenue Split Engine for Sovereignty Architecture
 * @dev Implements immutable revenue allocation with configurable recipients
 * 
 * The 7% split is distributed as follows:
 * - 40% (2.8% total) → Operations
 * - 30% (2.1% total) → Development  
 * - 20% (1.4% total) → Governance
 * - 10% (0.7% total) → Reserves
 */
contract SwarmGate {
    // Constants
    uint256 public constant TOTAL_SPLIT_BPS = 700;      // 7% in basis points
    uint256 public constant BPS_DENOMINATOR = 10000;
    
    uint256 public constant OPS_SHARE = 40;             // 40% of split
    uint256 public constant DEV_SHARE = 30;             // 30% of split
    uint256 public constant GOV_SHARE = 20;             // 20% of split
    uint256 public constant RESERVE_SHARE = 10;         // 10% of split
    uint256 public constant SHARE_DENOMINATOR = 100;

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
     * @notice Calculate split amounts for a given revenue
     * @param revenue The revenue amount to calculate split for
     */
    function calculateSplit(uint256 revenue) external pure returns (
        uint256 opsAmount,
        uint256 devAmount,
        uint256 govAmount,
        uint256 reserveAmount
    ) {
        uint256 splitAmount = (revenue * TOTAL_SPLIT_BPS) / BPS_DENOMINATOR;
        opsAmount = (splitAmount * OPS_SHARE) / SHARE_DENOMINATOR;
        devAmount = (splitAmount * DEV_SHARE) / SHARE_DENOMINATOR;
        govAmount = (splitAmount * GOV_SHARE) / SHARE_DENOMINATOR;
        reserveAmount = splitAmount - opsAmount - devAmount - govAmount;
    }

    /**
     * @dev Safe ETH transfer
     */
    function _safeTransfer(address to, uint256 amount) internal {
        (bool success, ) = to.call{value: amount}("");
        if (!success) revert TransferFailed();
    }
}
