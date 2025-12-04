// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title SwarmGateSplitter
 * @notice Sovereignty infrastructure that mathematically enforces a 7% charity tax.
 * @dev 93% forwarded to Ops immediately. 7% retained for quarterly distribution.
 *      Immutable: Charities cannot be removed after deployment.
 */
contract SwarmGateSplitter {
    // --- Configuration ---
    uint256 public constant CHARITY_BPS = 700; // 7%
    uint256 public constant BPS_DENOMINATOR = 10000;
    
    // The operational multisig (e.g., Gnosis Safe)
    address payable public immutable OPS_MULTISIG;
    
    // Hardcoded list of charities (St. Jude's, MSF, etc.)
    address payable[] public charities;
    
    // --- State ---
    uint256 public lastDistributionTime;
    uint256 public constant DISTRIBUTION_INTERVAL = 90 days;

    // --- Events ---
    event PaymentReceived(address indexed sender, uint256 amount, uint256 charityShare, uint256 opsShare);
    event OpsForwarded(uint256 amount);
    event CharityDistributed(uint256 totalDistributed, uint256 timestamp);

    // --- Errors ---
    error DistributionTooEarly();
    error NoFundsToDistribute();
    error TransferFailed();
    error CharityTransferFailed(uint256 charityIndex);

    constructor(address payable _opsMultisig, address payable[] memory _charities) {
        require(_opsMultisig != address(0), "Invalid Ops Address");
        require(_charities.length > 0, "No charities defined");
        
        OPS_MULTISIG = _opsMultisig;
        charities = _charities;
        lastDistributionTime = block.timestamp;
    }

    /**
     * @notice The Sink. Any ETH/Native Token sent here triggers the split.
     */
    receive() external payable {
        if (msg.value == 0) return;

        // Calculate 7% share
        uint256 charityShare = (msg.value * CHARITY_BPS) / BPS_DENOMINATOR;
        uint256 opsShare = msg.value - charityShare; // Remainder goes to Ops (handles dust)

        // 1. Forward 93% to Ops immediately
        (bool success, ) = OPS_MULTISIG.call{value: opsShare}("");
        if (!success) revert TransferFailed();
        
        emit OpsForwarded(opsShare);
        emit PaymentReceived(msg.sender, msg.value, charityShare, opsShare);
    }

    /**
     * @notice Distribute the accumulated 7% to the charity list.
     * @dev Callable by anyone (Keeper/Automation compatible).
     */
    function distributeCharity() external {
        if (block.timestamp < lastDistributionTime + DISTRIBUTION_INTERVAL) {
            revert DistributionTooEarly();
        }
        
        uint256 balance = address(this).balance;
        if (balance == 0) revert NoFundsToDistribute();

        uint256 sharePerCharity = balance / charities.length;
        if (sharePerCharity == 0) revert NoFundsToDistribute();

        // 2. Distribute pro-rata to charities
        uint256 distributed = 0;
        for (uint256 i = 0; i < charities.length; i++) {
            uint256 amount = sharePerCharity;
            // Give remainder to the last charity to avoid dust lockup
            if (i == charities.length - 1) {
                amount = balance - distributed;
            }
            (bool success, ) = charities[i].call{value: amount}("");
            if (!success) revert CharityTransferFailed(i);
            distributed += amount;
        }

        lastDistributionTime = block.timestamp;
        emit CharityDistributed(balance, block.timestamp);
    }
}
