// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title ImmutableCharitySplitter
 * @notice Sovereignty infrastructure that mathematically enforces a 7% charity tax.
 * @dev 93% is forwarded to Ops immediately. 7% is retained for quarterly distribution.
 */
contract ImmutableCharitySplitter {
    // --- Configuration ---
    uint256 public constant CHARITY_BPS = 700; // 7%
    uint256 public constant OPS_BPS = 9300;    // 93%
    uint256 public constant BPS_DENOMINATOR = 10000;

    address payable public immutable operationalMultisig;
    
    // --- State ---
    uint256 public totalCharityRaised;
    uint256 public totalOpsForwarded;
    
    // Charity Registry (Immutable once deployed, or use a registry pattern if charities change)
    // For v1.0, we hardcode the recipients to ensure trust.
    address payable[] public charities;
    
    // Distribution Logic
    uint256 public lastDistributionTime;
    uint256 public constant DISTRIBUTION_INTERVAL = 90 days;

    // --- Events ---
    event PaymentReceived(address indexed sender, uint256 amount, uint256 charityShare, uint256 opsShare);
    event OpsForwarded(address indexed recipient, uint256 amount);
    event CharityDistributed(uint256 totalDistributed, uint256 timestamp);

    // --- Errors ---
    error InvalidConfiguration();
    error DistributionTooEarly();
    error NoFundsToDistribute();
    error TransferFailed();

    constructor(address payable _operationalMultisig, address payable[] memory _charities) {
        if (_operationalMultisig == address(0) || _charities.length == 0) revert InvalidConfiguration();
        operationalMultisig = _operationalMultisig;
        charities = _charities;
        lastDistributionTime = block.timestamp;
    }

    /**
     * @notice The Sink. Any ETH sent here triggers the split.
     */
    receive() external payable {
        if (msg.value == 0) return;

        uint256 charityShare = (msg.value * CHARITY_BPS) / BPS_DENOMINATOR;
        uint256 opsShare = msg.value - charityShare; // Remainder goes to ops to avoid dust issues

        totalCharityRaised += charityShare;
        totalOpsForwarded += opsShare;

        emit PaymentReceived(msg.sender, msg.value, charityShare, opsShare);

        // Forward Ops share immediately
        (bool success, ) = operationalMultisig.call{value: opsShare}("");
        if (!success) revert TransferFailed();
        
        emit OpsForwarded(operationalMultisig, opsShare);
    }

    /**
     * @notice Distribute the accumulated 7% to the charity list.
     * @dev Callable by anyone (keeper/automation friendly).
     */
    function distributeCharity() external {
        if (block.timestamp < lastDistributionTime + DISTRIBUTION_INTERVAL) revert DistributionTooEarly();
        
        uint256 balance = address(this).balance;
        if (balance == 0) revert NoFundsToDistribute();

        uint256 sharePerCharity = balance / charities.length;
        if (sharePerCharity == 0) revert NoFundsToDistribute();

        for (uint256 i = 0; i < charities.length; i++) {
            (bool success, ) = charities[i].call{value: sharePerCharity}("");
            if (!success) revert TransferFailed();
        }

        lastDistributionTime = block.timestamp;
        emit CharityDistributed(balance, block.timestamp);
    }

    // Function to view pending balance for charities
    function pendingCharityBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
