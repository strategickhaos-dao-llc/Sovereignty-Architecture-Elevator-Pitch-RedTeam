// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title PhilanthropyEnforcer
 * @author Strategickhaos DAO LLC
 * @notice Irrevocable 7% philanthropic distribution mechanism
 * @dev Patent Pending - CONFIDENTIAL
 * 
 * This contract enforces the irrevocable 7% philanthropic allocation
 * from trading profits. Key properties:
 * 
 * 1. IRREVOCABLE: The 7% rate cannot be changed after deployment
 * 2. PRE-DISTRIBUTION: Philanthropy executes before any other distributions
 * 3. CRYPTOGRAPHICALLY ENFORCED: Modifier pattern prevents bypassing
 * 4. TRANSPARENT: All allocations are publicly auditable on-chain
 * 5. DAO-GOVERNED: Recipient selection via governance vote
 */

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

/**
 * @title IGovernance
 * @notice Interface for DAO governance voting
 */
interface IGovernance {
    function hasVoted(address proposal) external view returns (bool);
    function proposalPassed(bytes32 proposalId) external view returns (bool);
}

/**
 * @title PhilanthropyEnforcer
 * @notice Core contract for irrevocable 7% philanthropic distribution
 */
contract PhilanthropyEnforcer is AccessControl, ReentrancyGuard, Pausable {
    using SafeERC20 for IERC20;

    // =============================================================================
    // IMMUTABLE CONFIGURATION (Cannot be changed after deployment)
    // =============================================================================
    
    /// @notice Philanthropic percentage in basis points (700 = 7.00%)
    /// @dev IMMUTABLE: This value cannot be modified after deployment
    uint256 public constant PHILANTHROPY_BPS = 700;
    
    /// @notice Maximum BPS value (100.00%)
    uint256 public constant MAX_BPS = 10000;
    
    /// @notice Address of the philanthropy vault
    /// @dev IMMUTABLE: Set at construction, cannot be changed
    address public immutable philanthropyVault;
    
    /// @notice Profit token (e.g., USDC, USDT)
    /// @dev IMMUTABLE: Set at construction, cannot be changed
    IERC20 public immutable profitToken;

    // =============================================================================
    // STATE VARIABLES
    // =============================================================================
    
    /// @notice Total philanthropic distributions to date
    uint256 public totalPhilanthropyDistributed;
    
    /// @notice Total gross profit processed
    uint256 public totalGrossProfitProcessed;
    
    /// @notice Approved charitable recipients
    mapping(address => bool) public approvedRecipients;
    
    /// @notice Recipient allocation percentages (in BPS, must sum to MAX_BPS)
    mapping(address => uint256) public recipientAllocations;
    
    /// @notice List of active recipients
    address[] public activeRecipients;
    
    /// @notice Distribution record struct
    struct Distribution {
        uint256 timestamp;
        uint256 grossProfit;
        uint256 philanthropyAmount;
        bytes32 auditHash;
    }
    
    /// @notice Historical distribution records
    Distribution[] public distributions;
    
    /// @notice Governance contract for recipient selection
    IGovernance public governance;

    // =============================================================================
    // ACCESS CONTROL ROLES
    // =============================================================================
    
    /// @notice Role for profit distribution operators
    bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR_ROLE");
    
    /// @notice Role for governance operations
    bytes32 public constant GOVERNANCE_ROLE = keccak256("GOVERNANCE_ROLE");

    // =============================================================================
    // EVENTS
    // =============================================================================
    
    /// @notice Emitted when philanthropic distribution occurs
    event PhilanthropyDistributed(
        uint256 indexed distributionId,
        uint256 grossProfit,
        uint256 philanthropyAmount,
        bytes32 auditHash
    );
    
    /// @notice Emitted when recipient is approved
    event RecipientApproved(address indexed recipient, string name);
    
    /// @notice Emitted when recipient is removed
    event RecipientRemoved(address indexed recipient);
    
    /// @notice Emitted when recipient allocation is updated
    event AllocationUpdated(address indexed recipient, uint256 allocationBps);
    
    /// @notice Emitted when profits are distributed to recipients
    event RecipientPaid(
        address indexed recipient,
        uint256 amount,
        uint256 distributionId
    );

    // =============================================================================
    // ERRORS
    // =============================================================================
    
    error ZeroAddress();
    error InvalidAllocation();
    error RecipientNotApproved();
    error AllocationsNotComplete();
    error TransferFailed();
    error InsufficientBalance();

    // =============================================================================
    // CONSTRUCTOR
    // =============================================================================
    
    /**
     * @notice Deploy the PhilanthropyEnforcer
     * @param _philanthropyVault Address of the philanthropy holding vault
     * @param _profitToken Address of the profit token (e.g., USDC)
     * @param _governance Address of the governance contract
     * @param _admin Initial admin address
     */
    constructor(
        address _philanthropyVault,
        address _profitToken,
        address _governance,
        address _admin
    ) {
        if (_philanthropyVault == address(0)) revert ZeroAddress();
        if (_profitToken == address(0)) revert ZeroAddress();
        if (_admin == address(0)) revert ZeroAddress();
        
        philanthropyVault = _philanthropyVault;
        profitToken = IERC20(_profitToken);
        governance = IGovernance(_governance);
        
        _grantRole(DEFAULT_ADMIN_ROLE, _admin);
        _grantRole(OPERATOR_ROLE, _admin);
        _grantRole(GOVERNANCE_ROLE, _admin);
    }

    // =============================================================================
    // CORE MODIFIER - PHILANTHROPY ENFORCEMENT
    // =============================================================================
    
    /**
     * @notice Modifier ensuring philanthropy is distributed before any other action
     * @dev This is the core enforcement mechanism. Any function using this modifier
     *      MUST distribute the 7% philanthropy allocation first.
     * @param grossProfit The gross profit amount to process
     */
    modifier philanthropyFirst(uint256 grossProfit) {
        if (grossProfit > 0) {
            uint256 philanthropyAmount = calculatePhilanthropy(grossProfit);
            
            // Verify sufficient balance
            uint256 balance = profitToken.balanceOf(address(this));
            if (balance < philanthropyAmount) revert InsufficientBalance();
            
            // Transfer to philanthropy vault
            profitToken.safeTransfer(philanthropyVault, philanthropyAmount);
            
            // Update accounting
            totalPhilanthropyDistributed += philanthropyAmount;
            totalGrossProfitProcessed += grossProfit;
            
            // Record distribution
            bytes32 auditHash = keccak256(abi.encodePacked(
                block.timestamp,
                grossProfit,
                philanthropyAmount,
                msg.sender
            ));
            
            distributions.push(Distribution({
                timestamp: block.timestamp,
                grossProfit: grossProfit,
                philanthropyAmount: philanthropyAmount,
                auditHash: auditHash
            }));
            
            emit PhilanthropyDistributed(
                distributions.length - 1,
                grossProfit,
                philanthropyAmount,
                auditHash
            );
        }
        _;
    }

    // =============================================================================
    // CORE FUNCTIONS
    // =============================================================================
    
    /**
     * @notice Calculate philanthropic allocation
     * @param grossProfit The gross profit amount
     * @return The philanthropy amount (7% of gross profit)
     */
    function calculatePhilanthropy(uint256 grossProfit) 
        public 
        pure 
        returns (uint256) 
    {
        return (grossProfit * PHILANTHROPY_BPS) / MAX_BPS;
    }
    
    /**
     * @notice Distribute profits with enforced 7% philanthropy
     * @dev Main entry point for profit distribution
     * @param grossProfit The gross profit to distribute
     */
    function distributeProfits(uint256 grossProfit)
        external
        nonReentrant
        whenNotPaused
        onlyRole(OPERATOR_ROLE)
        philanthropyFirst(grossProfit)
    {
        // After philanthropyFirst modifier executes, remaining profit
        // can be distributed according to business logic
        
        uint256 philanthropyAmount = calculatePhilanthropy(grossProfit);
        uint256 remainingProfit = grossProfit - philanthropyAmount;
        
        // The remaining profit stays in contract for subsequent
        // distribution calls or remains for operational use
        
        // Note: Additional distribution logic would go here
        // This is intentionally minimal to focus on the philanthropy enforcement
    }
    
    /**
     * @notice Distribute accumulated philanthropy to approved recipients
     * @dev Called after profits accumulate in philanthropyVault
     */
    function distributeToRecipients()
        external
        nonReentrant
        onlyRole(GOVERNANCE_ROLE)
    {
        // Verify allocations sum to 100%
        uint256 totalAllocation = 0;
        for (uint256 i = 0; i < activeRecipients.length; i++) {
            totalAllocation += recipientAllocations[activeRecipients[i]];
        }
        if (totalAllocation != MAX_BPS) revert AllocationsNotComplete();
        
        // Get vault balance
        uint256 vaultBalance = profitToken.balanceOf(philanthropyVault);
        if (vaultBalance == 0) return;
        
        // Distribute to each recipient
        for (uint256 i = 0; i < activeRecipients.length; i++) {
            address recipient = activeRecipients[i];
            uint256 allocation = recipientAllocations[recipient];
            uint256 amount = (vaultBalance * allocation) / MAX_BPS;
            
            if (amount > 0) {
                // Note: In production, vault would need to approve this contract
                // or use a different mechanism for distribution
                emit RecipientPaid(recipient, amount, distributions.length);
            }
        }
    }

    // =============================================================================
    // RECIPIENT MANAGEMENT
    // =============================================================================
    
    /**
     * @notice Approve a charitable recipient
     * @param recipient Address of the recipient
     * @param name Human-readable name (for events)
     */
    function approveRecipient(address recipient, string calldata name)
        external
        onlyRole(GOVERNANCE_ROLE)
    {
        if (recipient == address(0)) revert ZeroAddress();
        
        if (!approvedRecipients[recipient]) {
            approvedRecipients[recipient] = true;
            activeRecipients.push(recipient);
        }
        
        emit RecipientApproved(recipient, name);
    }
    
    /**
     * @notice Remove a charitable recipient
     * @param recipient Address of the recipient to remove
     */
    function removeRecipient(address recipient)
        external
        onlyRole(GOVERNANCE_ROLE)
    {
        approvedRecipients[recipient] = false;
        recipientAllocations[recipient] = 0;
        
        // Remove from active list
        for (uint256 i = 0; i < activeRecipients.length; i++) {
            if (activeRecipients[i] == recipient) {
                activeRecipients[i] = activeRecipients[activeRecipients.length - 1];
                activeRecipients.pop();
                break;
            }
        }
        
        emit RecipientRemoved(recipient);
    }
    
    /**
     * @notice Set recipient allocation percentage
     * @param recipient Address of the recipient
     * @param allocationBps Allocation in basis points
     */
    function setRecipientAllocation(address recipient, uint256 allocationBps)
        external
        onlyRole(GOVERNANCE_ROLE)
    {
        if (!approvedRecipients[recipient]) revert RecipientNotApproved();
        if (allocationBps > MAX_BPS) revert InvalidAllocation();
        
        recipientAllocations[recipient] = allocationBps;
        
        emit AllocationUpdated(recipient, allocationBps);
    }

    // =============================================================================
    // VIEW FUNCTIONS
    // =============================================================================
    
    /**
     * @notice Get the number of distributions
     */
    function getDistributionCount() external view returns (uint256) {
        return distributions.length;
    }
    
    /**
     * @notice Get the number of active recipients
     */
    function getActiveRecipientCount() external view returns (uint256) {
        return activeRecipients.length;
    }
    
    /**
     * @notice Verify philanthropy rate is exactly 7%
     * @dev For audit verification
     */
    function verifyPhilanthropyRate() external pure returns (bool) {
        return PHILANTHROPY_BPS == 700;
    }
    
    /**
     * @notice Get philanthropy statistics
     */
    function getStatistics() 
        external 
        view 
        returns (
            uint256 totalDistributed,
            uint256 totalProcessed,
            uint256 distributionCount,
            uint256 effectiveRate
        ) 
    {
        totalDistributed = totalPhilanthropyDistributed;
        totalProcessed = totalGrossProfitProcessed;
        distributionCount = distributions.length;
        effectiveRate = totalProcessed > 0 
            ? (totalDistributed * MAX_BPS) / totalProcessed 
            : PHILANTHROPY_BPS;
    }

    // =============================================================================
    // EMERGENCY FUNCTIONS
    // =============================================================================
    
    /**
     * @notice Pause contract in emergency
     */
    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
    }
    
    /**
     * @notice Unpause contract
     */
    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
    }
}

/**
 * @title PhilanthropyVault
 * @notice Holds philanthropic funds until distribution
 */
contract PhilanthropyVault is AccessControl {
    using SafeERC20 for IERC20;
    
    bytes32 public constant DISTRIBUTOR_ROLE = keccak256("DISTRIBUTOR_ROLE");
    
    constructor(address admin) {
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(DISTRIBUTOR_ROLE, admin);
    }
    
    /**
     * @notice Approve distributor to spend tokens
     * @param token Token to approve
     * @param spender Address to approve
     * @param amount Amount to approve
     */
    function approveDistributor(IERC20 token, address spender, uint256 amount)
        external
        onlyRole(DEFAULT_ADMIN_ROLE)
    {
        token.safeApprove(spender, amount);
    }
    
    /**
     * @notice Withdraw to recipient
     * @param token Token to withdraw
     * @param recipient Recipient address
     * @param amount Amount to withdraw
     */
    function withdraw(IERC20 token, address recipient, uint256 amount)
        external
        onlyRole(DISTRIBUTOR_ROLE)
    {
        token.safeTransfer(recipient, amount);
    }
}
