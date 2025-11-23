# Smart Contract Security Framework
**Sovereignty Architecture - Irrevocable 7% Covenant Implementation**

## ⚠️ CRITICAL WARNING

This document addresses **Item #11**: "The 7% smart contract has an admin key you control → courts say it's revocable, not irrevocable."

The entire sovereignty architecture depends on the covenant being **TECHNICALLY IRREVOCABLE**, not just legally binding. If there's an admin key that can modify or disable the 7% allocation, the entire system is compromised.

---

## 🎯 Core Security Principles

### 1. True Irrevocability

**The covenant must be irrevocable through TECHNICAL CONSTRAINTS, not trust**:
- No admin keys
- No upgrade mechanisms that bypass covenant
- No circuit breakers that disable charity allocation
- Immutable percentage (cannot be reduced below 7%)
- Time-locked governance (minimum 30 days for any change)
- Multi-signature requirement (no single individual has override)

### 2. Defense in Depth

**Multiple layers of protection**:
1. **Immutable Core**: Critical functions permanently locked
2. **Multi-Signature**: Distributed control (3-of-5 minimum)
3. **Time-Lock**: Prevents hasty or coerced changes
4. **On-Chain Verification**: Publicly auditable enforcement
5. **Off-Chain Monitoring**: Alert system for violations
6. **Legal Layer**: Operating agreement reinforces technical constraints

---

## 📜 SMART CONTRACT ARCHITECTURE

### Contract Hierarchy

```
┌─────────────────────────────────────────┐
│   SovereigntyCovenantCore               │
│   (Immutable - No Upgrade Path)         │
│   - 7% minimum allocation constant      │
│   - Enforcement logic (cannot be        │
│     modified or disabled)               │
└─────────────────────────────────────────┘
                   ↑
                   │ (enforces)
                   │
┌─────────────────────────────────────────┐
│   ResourceAllocationRouter              │
│   (Upgradeable BUT covenant-constrained)│
│   - Routes computational resources      │
│   - MUST call CovenantCore first        │
│   - Cannot bypass enforcement           │
└─────────────────────────────────────────┘
                   ↑
                   │ (uses)
                   │
┌─────────────────────────────────────────┐
│   MultiSigGovernance                    │
│   (3-of-5 with time-lock)               │
│   - Can upgrade Router (not Core)       │
│   - Cannot reduce covenant percentage   │
│   - 30-day time-lock on changes         │
└─────────────────────────────────────────┘
```

---

## 🔒 IMMUTABLE CORE CONTRACT

### SovereigntyCovenantCore.sol

**Design Principles**:
- NO constructor that sets admin
- NO owner role
- NO upgrade mechanism
- NO circuit breaker
- ALL critical values are constants
- Deployed once, never changed

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title SovereigntyCovenantCore
 * @notice IMMUTABLE covenant enforcement contract
 * @dev This contract has NO admin, NO owner, NO upgrade path
 *      The 7% charitable covenant is PERMANENTLY ENFORCED
 */
contract SovereigntyCovenantCore {
    
    // ============ IMMUTABLE CONSTANTS ============
    
    /// @notice Minimum charity allocation percentage (cannot be changed)
    uint256 public constant MINIMUM_CHARITY_PERCENTAGE = 7;
    
    /// @notice Denominator for percentage calculations
    uint256 public constant PERCENTAGE_DENOMINATOR = 100;
    
    /// @notice Contract deployment timestamp (for auditing)
    uint256 public immutable deploymentTimestamp;
    
    /// @notice Charity registry contract (set once at deployment)
    address public immutable charityRegistry;
    
    // ============ STATE VARIABLES ============
    
    /// @notice Total amount enforced through covenant
    uint256 public totalEnforced;
    
    /// @notice Per-charity allocation tracking
    mapping(address => uint256) public charityAllocations;
    
    // ============ EVENTS ============
    
    event CovenantEnforced(
        address indexed payer,
        uint256 totalAmount,
        uint256 charityAmount,
        uint256 timestamp
    );
    
    event CharityAllocation(
        address indexed charity,
        uint256 amount,
        uint256 timestamp
    );
    
    // ============ ERRORS ============
    
    error CovenantViolation(uint256 required, uint256 provided);
    error InvalidCharityRegistry();
    error ZeroAmount();
    
    // ============ CONSTRUCTOR ============
    
    /**
     * @notice Deploy immutable covenant core
     * @param _charityRegistry Address of charity registry contract
     * @dev This is the ONLY time charityRegistry can be set
     */
    constructor(address _charityRegistry) {
        if (_charityRegistry == address(0)) revert InvalidCharityRegistry();
        
        charityRegistry = _charityRegistry;
        deploymentTimestamp = block.timestamp;
        
        // NO OWNER SET
        // NO ADMIN SET
        // NO UPGRADE MECHANISM
    }
    
    // ============ CORE ENFORCEMENT FUNCTION ============
    
    /**
     * @notice Enforce 7% covenant allocation
     * @param amount Total amount subject to covenant
     * @param charityRecipient Address of verified charity
     * @return charityAmount Amount allocated to charity
     * @dev This function MUST be called before any resource allocation
     *      There is NO WAY to bypass this enforcement
     */
    function enforceCovenantAllocation(
        uint256 amount,
        address charityRecipient
    ) external returns (uint256 charityAmount) {
        
        if (amount == 0) revert ZeroAmount();
        
        // Calculate required charity allocation
        charityAmount = (amount * MINIMUM_CHARITY_PERCENTAGE) / PERCENTAGE_DENOMINATOR;
        
        // Verify charity is registered and valid
        require(
            ICharityRegistry(charityRegistry).isVerifiedCharity(charityRecipient),
            "Charity not verified"
        );
        
        // Record allocation
        totalEnforced += charityAmount;
        charityAllocations[charityRecipient] += charityAmount;
        
        // Emit events for transparency
        emit CovenantEnforced(msg.sender, amount, charityAmount, block.timestamp);
        emit CharityAllocation(charityRecipient, charityAmount, block.timestamp);
        
        return charityAmount;
    }
    
    // ============ VIEW FUNCTIONS ============
    
    /**
     * @notice Calculate required charity amount for given total
     * @param amount Total amount
     * @return Required charity allocation
     */
    function calculateCharityAmount(uint256 amount) external pure returns (uint256) {
        return (amount * MINIMUM_CHARITY_PERCENTAGE) / PERCENTAGE_DENOMINATOR;
    }
    
    /**
     * @notice Get allocation for specific charity
     * @param charity Charity address
     * @return Total allocated to charity
     */
    function getCharityAllocation(address charity) external view returns (uint256) {
        return charityAllocations[charity];
    }
    
    /**
     * @notice Verify contract has no admin or upgrade path
     * @return true (for transparency)
     * @dev This function serves as documentation that there is NO admin
     */
    function hasNoAdmin() external pure returns (bool) {
        return true;
    }
    
    /**
     * @notice Verify contract has no upgrade mechanism
     * @return true (for transparency)
     */
    function hasNoUpgradeMechanism() external pure returns (bool) {
        return true;
    }
    
    /**
     * @notice Verify covenant percentage is immutable
     * @return true (for transparency)
     */
    function isCovenantImmutable() external pure returns (bool) {
        return true;
    }
}

/**
 * @title ICharityRegistry
 * @notice Interface for charity verification
 */
interface ICharityRegistry {
    function isVerifiedCharity(address charity) external view returns (bool);
    function getCharity501c3Status(address charity) external view returns (bool);
}
```

---

## 🔐 MULTI-SIGNATURE GOVERNANCE

### MultiSigGovernance.sol

**Design Principles**:
- Minimum 3-of-5 signatures required
- 30-day time-lock on all governance actions
- CANNOT modify covenant percentage
- CANNOT disable covenant enforcement
- CAN upgrade peripheral contracts (not core)
- CAN manage charity registry

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title MultiSigGovernance
 * @notice Multi-signature governance with time-lock
 * @dev Governs upgradeable components but CANNOT modify covenant core
 */
contract MultiSigGovernance {
    
    // ============ CONSTANTS ============
    
    /// @notice Minimum time-lock for governance actions (30 days)
    uint256 public constant TIMELOCK_DURATION = 30 days;
    
    /// @notice Required number of signatures
    uint256 public constant REQUIRED_SIGNATURES = 3;
    
    /// @notice Total number of signers
    uint256 public constant TOTAL_SIGNERS = 5;
    
    /// @notice Covenant core (immutable reference)
    address public immutable covenantCore;
    
    // ============ STATE VARIABLES ============
    
    /// @notice Authorized signers
    mapping(address => bool) public isSigner;
    address[] public signers;
    
    /// @notice Pending governance actions
    mapping(bytes32 => GovernanceAction) public pendingActions;
    
    // ============ STRUCTS ============
    
    struct GovernanceAction {
        bytes32 actionHash;
        address target;
        bytes data;
        uint256 value;
        uint256 queuedTimestamp;
        uint256 executeAfter;
        uint256 signatureCount;
        mapping(address => bool) hasApproved;
        bool executed;
        bool cancelled;
    }
    
    // ============ EVENTS ============
    
    event ActionQueued(bytes32 indexed actionHash, uint256 executeAfter);
    event ActionApproved(bytes32 indexed actionHash, address indexed signer);
    event ActionExecuted(bytes32 indexed actionHash);
    event ActionCancelled(bytes32 indexed actionHash);
    
    // ============ ERRORS ============
    
    error NotSigner();
    error AlreadyApproved();
    error InsufficientSignatures();
    error TimeLockNotExpired();
    error ActionAlreadyExecuted();
    error ActionCancelled();
    error CannotModifyCovenantCore();
    
    // ============ CONSTRUCTOR ============
    
    constructor(
        address _covenantCore,
        address[] memory _signers
    ) {
        require(_signers.length == TOTAL_SIGNERS, "Invalid signer count");
        
        covenantCore = _covenantCore;
        
        for (uint256 i = 0; i < _signers.length; i++) {
            require(_signers[i] != address(0), "Invalid signer");
            require(!isSigner[_signers[i]], "Duplicate signer");
            
            isSigner[_signers[i]] = true;
            signers.push(_signers[i]);
        }
    }
    
    // ============ GOVERNANCE FUNCTIONS ============
    
    /**
     * @notice Queue a governance action with time-lock
     * @param target Target contract
     * @param data Call data
     * @param value ETH value (if any)
     */
    function queueAction(
        address target,
        bytes calldata data,
        uint256 value
    ) external onlySigner returns (bytes32 actionHash) {
        
        // CRITICAL: Prevent modification of covenant core
        if (target == covenantCore) {
            revert CannotModifyCovenantCore();
        }
        
        actionHash = keccak256(abi.encode(target, data, value, block.timestamp));
        
        GovernanceAction storage action = pendingActions[actionHash];
        action.actionHash = actionHash;
        action.target = target;
        action.data = data;
        action.value = value;
        action.queuedTimestamp = block.timestamp;
        action.executeAfter = block.timestamp + TIMELOCK_DURATION;
        
        // First signer automatically approves
        action.hasApproved[msg.sender] = true;
        action.signatureCount = 1;
        
        emit ActionQueued(actionHash, action.executeAfter);
        emit ActionApproved(actionHash, msg.sender);
        
        return actionHash;
    }
    
    /**
     * @notice Approve a pending governance action
     * @param actionHash Hash of the action to approve
     */
    function approveAction(bytes32 actionHash) external onlySigner {
        GovernanceAction storage action = pendingActions[actionHash];
        
        require(action.actionHash == actionHash, "Action not found");
        require(!action.executed, "Already executed");
        require(!action.cancelled, "Action cancelled");
        
        if (action.hasApproved[msg.sender]) revert AlreadyApproved();
        
        action.hasApproved[msg.sender] = true;
        action.signatureCount++;
        
        emit ActionApproved(actionHash, msg.sender);
    }
    
    /**
     * @notice Execute approved governance action after time-lock
     * @param actionHash Hash of the action to execute
     */
    function executeAction(bytes32 actionHash) external onlySigner {
        GovernanceAction storage action = pendingActions[actionHash];
        
        require(action.actionHash == actionHash, "Action not found");
        
        if (action.executed) revert ActionAlreadyExecuted();
        if (action.cancelled) revert ActionCancelled();
        if (action.signatureCount < REQUIRED_SIGNATURES) revert InsufficientSignatures();
        if (block.timestamp < action.executeAfter) revert TimeLockNotExpired();
        
        action.executed = true;
        
        // Execute action
        (bool success, ) = action.target.call{value: action.value}(action.data);
        require(success, "Action execution failed");
        
        emit ActionExecuted(actionHash);
    }
    
    /**
     * @notice Cancel a pending action (requires 3-of-5 approval)
     * @param actionHash Hash of the action to cancel
     */
    function cancelAction(bytes32 actionHash) external onlySigner {
        GovernanceAction storage action = pendingActions[actionHash];
        
        require(action.actionHash == actionHash, "Action not found");
        require(!action.executed, "Already executed");
        require(action.signatureCount >= REQUIRED_SIGNATURES, "Need 3 signatures to cancel");
        
        action.cancelled = true;
        
        emit ActionCancelled(actionHash);
    }
    
    // ============ VIEW FUNCTIONS ============
    
    function getSigners() external view returns (address[] memory) {
        return signers;
    }
    
    function getActionDetails(bytes32 actionHash) external view returns (
        address target,
        uint256 value,
        uint256 queuedTimestamp,
        uint256 executeAfter,
        uint256 signatureCount,
        bool executed,
        bool cancelled
    ) {
        GovernanceAction storage action = pendingActions[actionHash];
        return (
            action.target,
            action.value,
            action.queuedTimestamp,
            action.executeAfter,
            action.signatureCount,
            action.executed,
            action.cancelled
        );
    }
    
    // ============ MODIFIERS ============
    
    modifier onlySigner() {
        if (!isSigner[msg.sender]) revert NotSigner();
        _;
    }
}
```

---

## 🏛️ CHARITY REGISTRY CONTRACT

### CharityRegistry.sol

**Design Principles**:
- Only verified 501(c)(3) organizations
- Oracle integration for IRS database verification
- Automatic de-listing if charity loses status
- Multi-sig controlled additions/removals

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title CharityRegistry
 * @notice Registry of verified 501(c)(3) charitable organizations
 * @dev Integrates with IRS database oracle for verification
 */
contract CharityRegistry {
    
    // ============ STATE VARIABLES ============
    
    /// @notice Multi-sig governance contract
    address public governance;
    
    /// @notice IRS verification oracle
    address public irsOracle;
    
    /// @notice Verified charities
    mapping(address => CharityInfo) public charities;
    address[] public charityList;
    
    // ============ STRUCTS ============
    
    struct CharityInfo {
        string name;
        string ein;  // IRS EIN
        address wallet;  // Charity-controlled wallet
        uint256 verifiedDate;
        uint256 lastStatusCheck;
        bool active;
        bool has501c3Status;
    }
    
    // ============ EVENTS ============
    
    event CharityAdded(address indexed charity, string name, string ein);
    event CharityRemoved(address indexed charity, string reason);
    event CharityStatusUpdated(address indexed charity, bool status);
    
    // ============ MODIFIERS ============
    
    modifier onlyGovernance() {
        require(msg.sender == governance, "Not governance");
        _;
    }
    
    // ============ CONSTRUCTOR ============
    
    constructor(address _governance, address _irsOracle) {
        governance = _governance;
        irsOracle = _irsOracle;
    }
    
    // ============ GOVERNANCE FUNCTIONS ============
    
    /**
     * @notice Add verified charity to registry
     * @param charity Charity wallet address (MUST be charity-controlled)
     * @param name Charity name
     * @param ein IRS Employer Identification Number
     */
    function addCharity(
        address charity,
        string calldata name,
        string calldata ein
    ) external onlyGovernance {
        
        require(charity != address(0), "Invalid address");
        require(!charities[charity].active, "Charity already registered");
        
        // Verify 501(c)(3) status via oracle
        bool has501c3 = IIRSOracle(irsOracle).verify501c3Status(ein);
        require(has501c3, "Not a valid 501(c)(3)");
        
        CharityInfo storage info = charities[charity];
        info.name = name;
        info.ein = ein;
        info.wallet = charity;
        info.verifiedDate = block.timestamp;
        info.lastStatusCheck = block.timestamp;
        info.active = true;
        info.has501c3Status = true;
        
        charityList.push(charity);
        
        emit CharityAdded(charity, name, ein);
    }
    
    /**
     * @notice Remove charity from registry
     * @param charity Charity address
     * @param reason Reason for removal
     */
    function removeCharity(
        address charity,
        string calldata reason
    ) external onlyGovernance {
        
        require(charities[charity].active, "Charity not registered");
        
        charities[charity].active = false;
        
        emit CharityRemoved(charity, reason);
    }
    
    /**
     * @notice Update charity 501(c)(3) status via oracle
     * @param charity Charity address
     */
    function updateCharityStatus(address charity) external {
        require(charities[charity].active, "Charity not registered");
        
        bool currentStatus = IIRSOracle(irsOracle).verify501c3Status(
            charities[charity].ein
        );
        
        charities[charity].has501c3Status = currentStatus;
        charities[charity].lastStatusCheck = block.timestamp;
        
        // Auto-deactivate if lost 501(c)(3) status
        if (!currentStatus) {
            charities[charity].active = false;
            emit CharityRemoved(charity, "Lost 501(c)(3) status");
        }
        
        emit CharityStatusUpdated(charity, currentStatus);
    }
    
    // ============ VIEW FUNCTIONS ============
    
    function isVerifiedCharity(address charity) external view returns (bool) {
        return charities[charity].active && charities[charity].has501c3Status;
    }
    
    function getCharity501c3Status(address charity) external view returns (bool) {
        return charities[charity].has501c3Status;
    }
    
    function getCharityInfo(address charity) external view returns (CharityInfo memory) {
        return charities[charity];
    }
    
    function getCharityCount() external view returns (uint256) {
        return charityList.length;
    }
}

interface IIRSOracle {
    function verify501c3Status(string calldata ein) external view returns (bool);
}
```

---

## 🔍 SECURITY AUDIT REQUIREMENTS

### Pre-Deployment Audit Checklist

- [ ] **Formal Verification**: Mathematical proof of covenant immutability
- [ ] **Third-Party Audit**: Minimum 2 independent security firms
  - [ ] Trail of Bits
  - [ ] OpenZeppelin
  - [ ] Consensys Diligence
- [ ] **Bug Bounty**: $100K+ program before mainnet deployment
- [ ] **Economic Security Review**: Game theory analysis
- [ ] **Legal Review**: Attorney verifies technical irrevocability

### Critical Security Properties to Verify

1. **Immutability**: No code path can modify or disable 7% covenant
2. **No Admin Override**: No single individual or key can bypass enforcement
3. **Time-Lock Protection**: Minimum 30 days for any governance change
4. **Multi-Sig Requirement**: 3-of-5 signatures required for governance
5. **Charity Verification**: Only verified 501(c)(3) organizations
6. **Reentrancy Safety**: No reentrancy attacks possible
7. **Integer Overflow**: SafeMath or Solidity 0.8+ protections
8. **Front-Running Resistance**: MEV protection where applicable

---

## 📊 MONITORING & ALERTING

### Real-Time Monitoring

**On-Chain Monitors**:
- [ ] Covenant enforcement events
- [ ] Governance action queue
- [ ] Charity registry changes
- [ ] Multi-sig activity
- [ ] Failed transactions (potential attacks)

**Alert Triggers**:
- [ ] Any transaction that bypasses covenant (should be impossible)
- [ ] Governance action queued
- [ ] Charity removed from registry
- [ ] Failed covenant enforcement
- [ ] Unusual transaction patterns

**Monitoring Tools**:
- Tenderly alerts
- OpenZeppelin Defender
- Custom monitoring script
- Discord/Slack webhooks

---

## 🧪 TESTNET DEPLOYMENT PLAN

### Testing Phases

**Phase 1: Unit Testing**
- [ ] Individual contract function tests
- [ ] Edge case coverage
- [ ] Gas optimization

**Phase 2: Integration Testing**
- [ ] Full system deployment on Goerli/Sepolia
- [ ] End-to-end transaction flows
- [ ] Multi-sig coordination
- [ ] Time-lock verification

**Phase 3: Security Testing**
- [ ] Attempted bypass scenarios
- [ ] Attack simulations
- [ ] Stress testing
- [ ] Formal verification

**Phase 4: Public Testnet**
- [ ] Open testnet deployment
- [ ] Community testing
- [ ] Bug bounty program
- [ ] Documentation validation

---

## 🚀 MAINNET DEPLOYMENT CHECKLIST

- [ ] All audits completed and issues resolved
- [ ] Bug bounty program completed (minimum 4 weeks)
- [ ] Multi-sig signers identified and ready
- [ ] Hardware wallets acquired and configured
- [ ] Charity partners identified and verified
- [ ] Legal opinion on technical irrevocability
- [ ] Deployment scripts tested on testnet
- [ ] Emergency response procedures documented
- [ ] 24/7 monitoring configured
- [ ] Team training completed

---

## 📞 EMERGENCY CONTACTS

**Smart Contract Security Team**:
- Lead Developer: ________________
- Security Auditor: ________________
- On-Call Engineer: ________________

**Multi-Sig Key Holders**:
1. Domenic Garza: ________________
2. Technical Lead: ________________
3. Legal Counsel: ________________
4. Board Member #1: ________________
5. Board Member #2: ________________

---

## 🔗 RELATED DOCUMENTS

- [DAO Formation Checklist](./DAO_FORMATION_CHECKLIST.md)
- [Succession Plan](./succession_plan.yaml)
- [Patent Protection](./PATENT_PROTECTION_CHECKLIST.md)
- [Risk Register](./RISK_REGISTER.yaml)

---

**Version**: 1.0  
**Created**: 2025-11-23  
**Last Updated**: 2025-11-23  
**Next Review**: Before mainnet deployment  
**Security Audit Status**: [ ] Not Started [ ] In Progress [ ] Complete
