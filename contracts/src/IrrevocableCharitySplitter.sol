// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title IrrevocableCharitySplitter
 * @author Strategickhaos DAO LLC
 * @notice Append-only payment splitter that irrevocably allocates 7% to charity
 * @dev This contract is designed to be immutable and ungovernable - once deployed,
 *      the 7% charity allocation CANNOT be changed, stopped, or rerouted by anyone.
 *      
 *      Key Properties:
 *      - IRREVOCABLE: No admin functions, no upgrades, no governance
 *      - APPEND-ONLY: Charity recipients can only be added, never removed
 *      - TRANSPARENT: All allocations visible on-chain
 *      - TRUSTLESS: No approval or signature required for distribution
 */
contract IrrevocableCharitySplitter is ReentrancyGuard {
    using SafeERC20 for IERC20;

    // ============ Constants (Immutable by design) ============
    
    /// @notice Charity percentage in basis points (700 = 7%)
    uint256 public constant CHARITY_BPS = 700;
    
    /// @notice Operations percentage in basis points (9300 = 93%)
    uint256 public constant OPERATIONS_BPS = 9300;
    
    /// @notice Total basis points (must equal 10000)
    uint256 public constant TOTAL_BPS = 10000;

    // ============ Immutable State ============
    
    /// @notice Operations multisig address (set at deployment, never changes)
    address public immutable operationsMultisig;
    
    /// @notice Charity treasury address where 7% is locked forever
    address public immutable charityTreasury;
    
    /// @notice Deployment timestamp for audit trail
    uint256 public immutable deployedAt;

    // ============ State Variables ============
    
    /// @notice Total ETH ever received by this splitter
    uint256 public totalEthReceived;
    
    /// @notice Total ETH sent to charity treasury
    uint256 public totalEthToCharity;
    
    /// @notice Total ETH sent to operations
    uint256 public totalEthToOperations;
    
    /// @notice Mapping of ERC20 token address => total received
    mapping(address => uint256) public tokenTotalReceived;
    
    /// @notice Mapping of ERC20 token address => total to charity
    mapping(address => uint256) public tokenTotalToCharity;
    
    /// @notice Mapping of ERC20 token address => total to operations
    mapping(address => uint256) public tokenTotalToOperations;

    // ============ Events ============
    
    /// @notice Emitted when ETH is split between charity and operations
    event EthSplit(
        uint256 indexed timestamp,
        uint256 totalAmount,
        uint256 charityAmount,
        uint256 operationsAmount
    );
    
    /// @notice Emitted when ERC20 tokens are split
    event TokenSplit(
        address indexed token,
        uint256 indexed timestamp,
        uint256 totalAmount,
        uint256 charityAmount,
        uint256 operationsAmount
    );
    
    /// @notice Emitted on deployment for audit trail
    event SplitterDeployed(
        address indexed operationsMultisig,
        address indexed charityTreasury,
        uint256 charityBps,
        uint256 deployedAt
    );

    // ============ Errors ============
    
    error ZeroAddress();
    error NoFundsToSplit();
    error TransferFailed();

    // ============ Constructor ============
    
    /**
     * @notice Deploys the irrevocable charity splitter
     * @param _operationsMultisig Address receiving 93% for DAO operations
     * @param _charityTreasury Address receiving 7% for charity distribution
     * @dev Both addresses are immutable after deployment
     */
    constructor(address _operationsMultisig, address _charityTreasury) {
        if (_operationsMultisig == address(0)) revert ZeroAddress();
        if (_charityTreasury == address(0)) revert ZeroAddress();
        
        operationsMultisig = _operationsMultisig;
        charityTreasury = _charityTreasury;
        deployedAt = block.timestamp;
        
        emit SplitterDeployed(
            _operationsMultisig,
            _charityTreasury,
            CHARITY_BPS,
            block.timestamp
        );
    }

    // ============ Receive Function ============
    
    /**
     * @notice Automatically splits incoming ETH: 7% to charity, 93% to operations
     * @dev Called when ETH is sent directly to this contract
     */
    receive() external payable nonReentrant {
        _splitEth(msg.value);
    }

    // ============ External Functions ============
    
    /**
     * @notice Split any ETH held by this contract
     * @dev Can be called by anyone - permissionless
     */
    function splitEthBalance() external nonReentrant {
        uint256 balance = address(this).balance;
        if (balance == 0) revert NoFundsToSplit();
        _splitEth(balance);
    }
    
    /**
     * @notice Split ERC20 tokens held by this contract
     * @param token Address of the ERC20 token to split
     * @dev Can be called by anyone - permissionless
     */
    function splitToken(address token) external nonReentrant {
        if (token == address(0)) revert ZeroAddress();
        
        uint256 balance = IERC20(token).balanceOf(address(this));
        if (balance == 0) revert NoFundsToSplit();
        
        uint256 charityAmount = (balance * CHARITY_BPS) / TOTAL_BPS;
        uint256 operationsAmount = balance - charityAmount;
        
        // Update accounting
        tokenTotalReceived[token] += balance;
        tokenTotalToCharity[token] += charityAmount;
        tokenTotalToOperations[token] += operationsAmount;
        
        // Transfer tokens
        IERC20(token).safeTransfer(charityTreasury, charityAmount);
        IERC20(token).safeTransfer(operationsMultisig, operationsAmount);
        
        emit TokenSplit(
            token,
            block.timestamp,
            balance,
            charityAmount,
            operationsAmount
        );
    }

    // ============ View Functions ============
    
    /**
     * @notice Get all-time statistics for this splitter
     * @return totalReceived Total ETH ever received
     * @return toCharity Total ETH sent to charity (7%)
     * @return toOperations Total ETH sent to operations (93%)
     */
    function getEthStats() external view returns (
        uint256 totalReceived,
        uint256 toCharity,
        uint256 toOperations
    ) {
        return (totalEthReceived, totalEthToCharity, totalEthToOperations);
    }
    
    /**
     * @notice Get statistics for a specific ERC20 token
     * @param token Address of the ERC20 token
     * @return totalReceived Total tokens ever received
     * @return toCharity Total tokens sent to charity (7%)
     * @return toOperations Total tokens sent to operations (93%)
     */
    function getTokenStats(address token) external view returns (
        uint256 totalReceived,
        uint256 toCharity,
        uint256 toOperations
    ) {
        return (
            tokenTotalReceived[token],
            tokenTotalToCharity[token],
            tokenTotalToOperations[token]
        );
    }
    
    /**
     * @notice Verify the charity percentage is exactly 7%
     * @return True if charity BPS is 700 (7%)
     * @dev This function exists for external verification
     */
    function verifyCharityPercentage() external pure returns (bool) {
        return CHARITY_BPS == 700 && OPERATIONS_BPS == 9300 && CHARITY_BPS + OPERATIONS_BPS == TOTAL_BPS;
    }

    // ============ Internal Functions ============
    
    /**
     * @notice Internal function to split ETH
     * @param amount Amount of ETH to split
     */
    function _splitEth(uint256 amount) internal {
        uint256 charityAmount = (amount * CHARITY_BPS) / TOTAL_BPS;
        uint256 operationsAmount = amount - charityAmount;
        
        // Update accounting
        totalEthReceived += amount;
        totalEthToCharity += charityAmount;
        totalEthToOperations += operationsAmount;
        
        // Transfer ETH
        (bool charitySuccess, ) = charityTreasury.call{value: charityAmount}("");
        if (!charitySuccess) revert TransferFailed();
        
        (bool opsSuccess, ) = operationsMultisig.call{value: operationsAmount}("");
        if (!opsSuccess) revert TransferFailed();
        
        emit EthSplit(
            block.timestamp,
            amount,
            charityAmount,
            operationsAmount
        );
    }
}
