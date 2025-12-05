// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

/**
 * @title CourseForgeToken
 * @author Strategickhaos DAO LLC / Valoryield Engine
 * @notice CFT - Crystallized XP for the Hogwarts Protocol
 * @dev Non-speculative utility token for:
 *      - Recording completed educational work (XP)
 *      - Unlocking platform features
 *      - Governance voting weight
 *      - Accounting anchor for CPA compliance
 * 
 * By default, CFT is non-transferable (soulbound) to prevent speculation.
 * Platform admin can enable transfers if needed for specific use cases.
 */
contract CourseForgeToken is ERC20, ERC20Burnable, AccessControl {
    
    // ============================================
    // ROLES
    // ============================================
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant PLATFORM_ROLE = keccak256("PLATFORM_ROLE");
    
    // ============================================
    // STATE
    // ============================================
    
    // Transfer restrictions
    bool public transfersEnabled;
    
    // Governance staking
    mapping(address => uint256) public stakedBalance;
    mapping(address => uint256) public stakingTimestamp;
    
    // Lifetime stats
    mapping(address => uint256) public lifetimeEarned;
    mapping(address => uint256) public lifetimeSpent;
    
    // Platform name for off-chain tracking
    string public constant PLATFORM_NAME = "CourseQuest Hogwarts";
    
    // ============================================
    // EVENTS
    // ============================================
    
    /**
     * @notice Emitted when CFT is minted for completed work
     */
    event CFTMinted(
        address indexed to,
        uint256 amount,
        string referenceType,
        string referenceId,
        string reason
    );
    
    /**
     * @notice Emitted when CFT is staked for governance
     */
    event CFTStaked(address indexed account, uint256 amount);
    
    /**
     * @notice Emitted when CFT is unstaked from governance
     */
    event CFTUnstaked(address indexed account, uint256 amount);
    
    /**
     * @notice Emitted when CFT is spent on platform features
     */
    event CFTSpent(address indexed account, uint256 amount, string feature);
    
    /**
     * @notice Emitted when transfer mode is changed
     */
    event TransfersEnabled(bool enabled);

    // ============================================
    // CONSTRUCTOR
    // ============================================
    
    /**
     * @notice Initialize CourseForge Token
     * @param _transfersEnabled Whether to allow transfers initially (false = soulbound)
     */
    constructor(bool _transfersEnabled) ERC20("CourseForge Token", "CFT") {
        transfersEnabled = _transfersEnabled;
        
        // Grant roles to deployer
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        _grantRole(PLATFORM_ROLE, msg.sender);
    }

    // ============================================
    // MINTING FUNCTIONS
    // ============================================
    
    /**
     * @notice Mint CFT to a student for completed work
     * @param _to Recipient address
     * @param _amount Amount of CFT to mint (typically = XP earned)
     * @param _referenceType Type of reference (e.g., "spell", "course")
     * @param _referenceId Off-chain ID of the reference
     * @param _reason Human-readable reason for minting
     */
    function mint(
        address _to,
        uint256 _amount,
        string calldata _referenceType,
        string calldata _referenceId,
        string calldata _reason
    ) external onlyRole(MINTER_ROLE) {
        require(_to != address(0), "Cannot mint to zero address");
        require(_amount > 0, "Amount must be positive");
        
        _mint(_to, _amount);
        lifetimeEarned[_to] += _amount;
        
        emit CFTMinted(_to, _amount, _referenceType, _referenceId, _reason);
    }
    
    /**
     * @notice Batch mint CFT to multiple recipients
     * @dev Gas optimization for bulk minting (e.g., end-of-course rewards)
     */
    function batchMint(
        address[] calldata _recipients,
        uint256[] calldata _amounts,
        string calldata _referenceType,
        string[] calldata _referenceIds,
        string calldata _reason
    ) external onlyRole(MINTER_ROLE) {
        require(_recipients.length == _amounts.length, "Array length mismatch");
        require(_recipients.length == _referenceIds.length, "Array length mismatch");
        
        for (uint256 i = 0; i < _recipients.length; i++) {
            require(_recipients[i] != address(0), "Cannot mint to zero address");
            require(_amounts[i] > 0, "Amount must be positive");
            
            _mint(_recipients[i], _amounts[i]);
            lifetimeEarned[_recipients[i]] += _amounts[i];
            
            emit CFTMinted(_recipients[i], _amounts[i], _referenceType, _referenceIds[i], _reason);
        }
    }

    // ============================================
    // STAKING FUNCTIONS (Governance)
    // ============================================
    
    /**
     * @notice Stake CFT for governance voting power
     * @param _amount Amount to stake
     */
    function stake(uint256 _amount) external {
        require(_amount > 0, "Amount must be positive");
        require(balanceOf(msg.sender) >= _amount, "Insufficient balance");
        
        // Move tokens to staked balance (burn from liquid, track in mapping)
        _burn(msg.sender, _amount);
        stakedBalance[msg.sender] += _amount;
        stakingTimestamp[msg.sender] = block.timestamp;
        
        emit CFTStaked(msg.sender, _amount);
    }
    
    /**
     * @notice Unstake CFT from governance
     * @param _amount Amount to unstake
     */
    function unstake(uint256 _amount) external {
        require(_amount > 0, "Amount must be positive");
        require(stakedBalance[msg.sender] >= _amount, "Insufficient staked balance");
        
        // Return tokens from staked balance
        stakedBalance[msg.sender] -= _amount;
        _mint(msg.sender, _amount);
        
        emit CFTUnstaked(msg.sender, _amount);
    }
    
    /**
     * @notice Get total balance (liquid + staked)
     */
    function totalBalanceOf(address _account) external view returns (uint256) {
        return balanceOf(_account) + stakedBalance[_account];
    }
    
    /**
     * @notice Get governance weight (currently = staked balance)
     * @dev Future versions may add time-weighted voting
     */
    function governanceWeight(address _account) external view returns (uint256) {
        return stakedBalance[_account];
    }

    // ============================================
    // SPENDING FUNCTIONS
    // ============================================
    
    /**
     * @notice Spend CFT on platform features
     * @param _amount Amount to spend
     * @param _feature Feature being purchased
     */
    function spend(uint256 _amount, string calldata _feature) external {
        require(_amount > 0, "Amount must be positive");
        require(balanceOf(msg.sender) >= _amount, "Insufficient balance");
        
        _burn(msg.sender, _amount);
        lifetimeSpent[msg.sender] += _amount;
        
        emit CFTSpent(msg.sender, _amount, _feature);
    }
    
    /**
     * @notice Platform-initiated spending (for automated feature unlocks)
     */
    function platformSpend(
        address _account, 
        uint256 _amount, 
        string calldata _feature
    ) external onlyRole(PLATFORM_ROLE) {
        require(_amount > 0, "Amount must be positive");
        require(balanceOf(_account) >= _amount, "Insufficient balance");
        
        _burn(_account, _amount);
        lifetimeSpent[_account] += _amount;
        
        emit CFTSpent(_account, _amount, _feature);
    }

    // ============================================
    // ADMIN FUNCTIONS
    // ============================================
    
    /**
     * @notice Enable or disable token transfers
     * @dev When disabled, CFT is soulbound (non-transferable)
     */
    function setTransfersEnabled(bool _enabled) external onlyRole(DEFAULT_ADMIN_ROLE) {
        transfersEnabled = _enabled;
        emit TransfersEnabled(_enabled);
    }
    
    /**
     * @notice Add a minter
     */
    function addMinter(address _minter) external onlyRole(DEFAULT_ADMIN_ROLE) {
        grantRole(MINTER_ROLE, _minter);
    }
    
    /**
     * @notice Remove a minter
     */
    function removeMinter(address _minter) external onlyRole(DEFAULT_ADMIN_ROLE) {
        revokeRole(MINTER_ROLE, _minter);
    }

    // ============================================
    // OVERRIDE FUNCTIONS
    // ============================================
    
    /**
     * @notice Override transfer to enforce soulbound mode
     */
    function _update(
        address from,
        address to,
        uint256 value
    ) internal override {
        // Allow minting (from == 0) and burning (to == 0) always
        // Block transfers if transfers are disabled
        if (from != address(0) && to != address(0) && !transfersEnabled) {
            revert("CFT: transfers are disabled (soulbound mode)");
        }
        
        super._update(from, to, value);
    }
    
    /**
     * @notice Get decimals (matching standard token convention)
     * @dev Using 18 decimals for precision in calculations
     */
    function decimals() public pure override returns (uint8) {
        return 18;
    }
}
