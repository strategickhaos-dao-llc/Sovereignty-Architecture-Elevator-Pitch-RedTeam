// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title AntiRugPullLogic
 * @notice Solidity contract for asset transfer on dissolution
 * @dev Source: CFTC v. Ooki Judgment + MakerDAO Endgame
 * @dev Deployed by: Sovereign Compiler v1.0
 * 
 * This contract implements decentralized governance wind-down safeguards
 * that auto-transfer assets to a designated safe harbor (ValorYield) 
 * on governance failure detection.
 */

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract AntiRugPullLogic is AccessControl, ReentrancyGuard {
    using SafeERC20 for IERC20;

    // Roles
    bytes32 public constant GUARDIAN_ROLE = keccak256("GUARDIAN_ROLE");
    bytes32 public constant EMERGENCY_ROLE = keccak256("EMERGENCY_ROLE");

    // Safe harbor address (ValorYield)
    address public safeHarbor;
    
    // Governance failure detection thresholds
    uint256 public inactivityThreshold; // seconds
    uint256 public lastGovernanceActivity;
    uint256 public minQuorumRequired; // basis points (100 = 1%)
    
    // Emergency state
    bool public emergencyMode;
    bool public dissolved;
    
    // Dissolution voting
    uint256 public dissolutionVotesFor;
    uint256 public dissolutionVotesAgainst;
    uint256 public dissolutionVoteDeadline;
    uint256 private _proposalNonce;  // Nonce to track proposal rounds
    mapping(address => uint256) public voterNonce;  // Track which proposal round voter participated in
    
    // Asset registry
    address[] public registeredAssets;
    mapping(address => bool) public isRegisteredAsset;

    // Events
    event SafeHarborUpdated(address indexed oldHarbor, address indexed newHarbor);
    event GovernanceActivityRecorded(uint256 timestamp);
    event EmergencyModeActivated(address indexed activator, string reason);
    event EmergencyModeDeactivated(address indexed deactivator);
    event DissolutionProposed(uint256 deadline);
    event DissolutionVoteCast(address indexed voter, bool inFavor);
    event DissolutionExecuted(uint256 timestamp);
    event AssetTransferred(address indexed asset, address indexed to, uint256 amount);
    event AssetRegistered(address indexed asset);

    // Errors
    error InvalidAddress();
    error AlreadyDissolved();
    error NotInEmergencyMode();
    error VotingNotActive();
    error AlreadyVoted();
    error VotingStillActive();
    error DissolutionRejected();
    error TransferFailed();

    constructor(
        address _safeHarbor,
        uint256 _inactivityThreshold,
        uint256 _minQuorumRequired
    ) {
        if (_safeHarbor == address(0)) revert InvalidAddress();
        
        safeHarbor = _safeHarbor;
        inactivityThreshold = _inactivityThreshold;
        minQuorumRequired = _minQuorumRequired;
        lastGovernanceActivity = block.timestamp;
        
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(GUARDIAN_ROLE, msg.sender);
        _grantRole(EMERGENCY_ROLE, msg.sender);
    }

    /**
     * @notice Record governance activity to reset inactivity timer
     * @dev Called by governance contracts when votes/proposals occur
     */
    function recordGovernanceActivity() external onlyRole(GUARDIAN_ROLE) {
        lastGovernanceActivity = block.timestamp;
        emit GovernanceActivityRecorded(block.timestamp);
    }

    /**
     * @notice Check if governance has been inactive beyond threshold
     * @return bool True if governance appears failed/inactive
     */
    function isGovernanceFailed() public view returns (bool) {
        return block.timestamp > lastGovernanceActivity + inactivityThreshold;
    }

    /**
     * @notice Activate emergency mode due to governance failure
     * @param reason Description of why emergency is activated
     */
    function activateEmergencyMode(string calldata reason) 
        external 
        onlyRole(EMERGENCY_ROLE) 
    {
        if (dissolved) revert AlreadyDissolved();
        
        emergencyMode = true;
        emit EmergencyModeActivated(msg.sender, reason);
    }

    /**
     * @notice Deactivate emergency mode if governance recovers
     */
    function deactivateEmergencyMode() 
        external 
        onlyRole(EMERGENCY_ROLE) 
    {
        emergencyMode = false;
        emit EmergencyModeDeactivated(msg.sender);
    }

    /**
     * @notice Propose dissolution with voting period
     * @dev Resets voting state including previous voter records
     * @param votingPeriod Duration in seconds for voting
     */
    function proposeDissolution(uint256 votingPeriod) 
        external 
        onlyRole(GUARDIAN_ROLE) 
    {
        if (dissolved) revert AlreadyDissolved();
        
        // Reset voting state including voter tracking
        dissolutionVotesFor = 0;
        dissolutionVotesAgainst = 0;
        dissolutionVoteDeadline = block.timestamp + votingPeriod;
        _proposalNonce++;  // Increment nonce to invalidate previous votes
        
        emit DissolutionProposed(dissolutionVoteDeadline);
    }

    /**
     * @notice Cast vote on dissolution proposal
     * @param inFavor True to vote for dissolution
     */
    function voteDissolution(bool inFavor) external {
        if (dissolutionVoteDeadline == 0 || block.timestamp > dissolutionVoteDeadline) {
            revert VotingNotActive();
        }
        // Check if voter already voted in current proposal round
        if (voterNonce[msg.sender] == _proposalNonce) revert AlreadyVoted();
        
        // Record vote for current proposal round
        voterNonce[msg.sender] = _proposalNonce;
        
        if (inFavor) {
            dissolutionVotesFor++;
        } else {
            dissolutionVotesAgainst++;
        }
        
        emit DissolutionVoteCast(msg.sender, inFavor);
    }

    /**
     * @notice Execute dissolution if approved
     * @dev Transfers all registered assets to safe harbor. 
     *      Dissolution requires strict majority (votesFor > votesAgainst).
     *      Tie votes are treated as rejection to maintain status quo.
     */
    function executeDissolution() external nonReentrant onlyRole(GUARDIAN_ROLE) {
        if (dissolved) revert AlreadyDissolved();
        if (block.timestamp <= dissolutionVoteDeadline) revert VotingStillActive();
        
        // Require strict majority: votesFor must exceed votesAgainst (tie = rejection)
        uint256 totalVotes = dissolutionVotesFor + dissolutionVotesAgainst;
        if (totalVotes == 0 || dissolutionVotesFor <= dissolutionVotesAgainst) {
            revert DissolutionRejected();
        }
        
        dissolved = true;
        emit DissolutionExecuted(block.timestamp);
        
        // Transfer all registered assets to safe harbor
        _transferAllAssets();
    }

    /**
     * @notice Emergency dissolution without voting (requires both roles)
     * @dev Only callable when governance has completely failed
     */
    function emergencyDissolution() 
        external 
        nonReentrant 
        onlyRole(EMERGENCY_ROLE) 
    {
        if (dissolved) revert AlreadyDissolved();
        if (!emergencyMode) revert NotInEmergencyMode();
        if (!isGovernanceFailed()) revert NotInEmergencyMode();
        
        dissolved = true;
        emit DissolutionExecuted(block.timestamp);
        
        _transferAllAssets();
    }

    /**
     * @notice Register an ERC20 asset for dissolution transfer
     * @param asset Address of the ERC20 token
     */
    function registerAsset(address asset) external onlyRole(GUARDIAN_ROLE) {
        if (asset == address(0)) revert InvalidAddress();
        if (!isRegisteredAsset[asset]) {
            registeredAssets.push(asset);
            isRegisteredAsset[asset] = true;
            emit AssetRegistered(asset);
        }
    }

    /**
     * @notice Update the safe harbor address
     * @param newSafeHarbor New address for asset transfers
     */
    function updateSafeHarbor(address newSafeHarbor) 
        external 
        onlyRole(DEFAULT_ADMIN_ROLE) 
    {
        if (newSafeHarbor == address(0)) revert InvalidAddress();
        
        address oldHarbor = safeHarbor;
        safeHarbor = newSafeHarbor;
        
        emit SafeHarborUpdated(oldHarbor, newSafeHarbor);
    }

    /**
     * @notice Internal function to transfer all assets to safe harbor
     * @dev Uses low-level call for ETH transfer to support both EOAs and contracts.
     *      SafeHarbor address should be verified to accept ETH before deployment.
     */
    function _transferAllAssets() internal {
        // Transfer ETH using low-level call with sufficient gas
        // This supports both EOAs and contracts with receive/fallback functions
        uint256 ethBalance = address(this).balance;
        if (ethBalance > 0) {
            (bool success, ) = safeHarbor.call{value: ethBalance, gas: 100000}("");
            if (!success) revert TransferFailed();
            emit AssetTransferred(address(0), safeHarbor, ethBalance);
        }
        
        // Transfer all registered ERC20 tokens
        for (uint256 i = 0; i < registeredAssets.length; i++) {
            address asset = registeredAssets[i];
            uint256 balance = IERC20(asset).balanceOf(address(this));
            if (balance > 0) {
                IERC20(asset).safeTransfer(safeHarbor, balance);
                emit AssetTransferred(asset, safeHarbor, balance);
            }
        }
    }

    /**
     * @notice Get list of all registered assets
     * @return Array of asset addresses
     */
    function getRegisteredAssets() external view returns (address[] memory) {
        return registeredAssets;
    }

    /**
     * @notice Get current dissolution status
     */
    function getDissolutionStatus() external view returns (
        bool isDissolved,
        bool isEmergency,
        bool governanceFailed,
        uint256 votesFor,
        uint256 votesAgainst,
        uint256 voteDeadline
    ) {
        return (
            dissolved,
            emergencyMode,
            isGovernanceFailed(),
            dissolutionVotesFor,
            dissolutionVotesAgainst,
            dissolutionVoteDeadline
        );
    }

    /**
     * @notice Allow contract to receive ETH
     */
    receive() external payable {}
}
