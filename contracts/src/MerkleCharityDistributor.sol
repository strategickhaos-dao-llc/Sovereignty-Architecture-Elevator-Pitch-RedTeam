// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title MerkleCharityDistributor
 * @author Strategickhaos DAO LLC
 * @notice Distributes charity funds pro-rata to pre-named charities using Merkle proofs
 * @dev This is the "charity treasury" that receives 7% from the IrrevocableCharitySplitter.
 *      Funds are distributed quarterly to verified charity addresses using a Merkle tree.
 *      
 *      Key Properties:
 *      - APPEND-ONLY: Charities can only be added to future distributions, never removed from past ones
 *      - TRANSPARENT: All distributions verifiable on-chain
 *      - PERMISSIONLESS: Anyone can trigger quarterly distributions
 *      - AUDITABLE: Full history of all charity payments
 */
contract MerkleCharityDistributor is ReentrancyGuard {
    using SafeERC20 for IERC20;

    // ============ Structs ============
    
    /// @notice Represents a distribution epoch (quarterly)
    struct Epoch {
        bytes32 merkleRoot;
        uint256 totalAmount;
        uint256 distributedAmount;
        uint256 startTime;
        uint256 endTime;
        bool finalized;
    }
    
    /// @notice Charity recipient info
    struct CharityInfo {
        string name;
        string ein; // IRS Employer Identification Number
        uint256 allocationBps; // Basis points out of 10000
        bool active;
    }

    // ============ Constants ============
    
    /// @notice Minimum time between distributions (90 days = quarterly)
    uint256 public constant DISTRIBUTION_INTERVAL = 90 days;
    
    /// @notice Total basis points for allocation
    uint256 public constant TOTAL_BPS = 10000;

    // ============ Immutable State ============
    
    /// @notice Address that can update Merkle roots (should be a multisig or DAO)
    address public immutable rootUpdater;
    
    /// @notice Deployment timestamp
    uint256 public immutable deployedAt;

    // ============ State Variables ============
    
    /// @notice Current epoch number
    uint256 public currentEpoch;
    
    /// @notice Last distribution timestamp
    uint256 public lastDistributionTime;
    
    /// @notice Mapping of epoch number => Epoch data
    mapping(uint256 => Epoch) public epochs;
    
    /// @notice Mapping of epoch => charity address => claimed (for ETH)
    mapping(uint256 => mapping(address => bool)) public claimed;
    
    /// @notice Mapping of epoch => token => charity address => claimed (for ERC20)
    mapping(uint256 => mapping(address => mapping(address => bool))) public tokenClaimed;
    
    /// @notice Total ETH ever distributed to charities
    uint256 public totalEthDistributed;
    
    /// @notice Mapping of ERC20 token => total distributed
    mapping(address => uint256) public totalTokenDistributed;
    
    /// @notice Array of registered charity addresses (append-only)
    address[] public registeredCharities;
    
    /// @notice Mapping of charity address => info
    mapping(address => CharityInfo) public charityInfo;

    // ============ Events ============
    
    event EpochCreated(
        uint256 indexed epochNumber,
        bytes32 merkleRoot,
        uint256 totalAmount,
        uint256 startTime
    );
    
    event CharityRegistered(
        address indexed charityAddress,
        string name,
        string ein,
        uint256 allocationBps
    );
    
    event FundsClaimed(
        uint256 indexed epochNumber,
        address indexed charity,
        uint256 amount,
        address token // address(0) for ETH
    );
    
    event EpochFinalized(
        uint256 indexed epochNumber,
        uint256 totalDistributed
    );

    // ============ Errors ============
    
    error ZeroAddress();
    error InvalidProof();
    error AlreadyClaimed();
    error EpochNotActive();
    error TooEarlyForDistribution();
    error InvalidAllocation();
    error NotRootUpdater();
    error CharityAlreadyRegistered();

    // ============ Modifiers ============
    
    modifier onlyRootUpdater() {
        if (msg.sender != rootUpdater) revert NotRootUpdater();
        _;
    }

    // ============ Constructor ============
    
    /**
     * @notice Deploy the Merkle charity distributor
     * @param _rootUpdater Address authorized to update Merkle roots (multisig recommended)
     */
    constructor(address _rootUpdater) {
        if (_rootUpdater == address(0)) revert ZeroAddress();
        rootUpdater = _rootUpdater;
        deployedAt = block.timestamp;
        lastDistributionTime = block.timestamp;
    }

    // ============ Receive Function ============
    
    /**
     * @notice Accept ETH deposits (from CharitySplitter)
     */
    receive() external payable {}

    // ============ External Functions ============
    
    /**
     * @notice Register a new charity recipient (append-only)
     * @param charityAddress Wallet address of the charity
     * @param name Official charity name
     * @param ein IRS EIN for verification
     * @param allocationBps Allocation in basis points
     */
    function registerCharity(
        address charityAddress,
        string calldata name,
        string calldata ein,
        uint256 allocationBps
    ) external onlyRootUpdater {
        if (charityAddress == address(0)) revert ZeroAddress();
        if (charityInfo[charityAddress].active) revert CharityAlreadyRegistered();
        if (allocationBps == 0 || allocationBps > TOTAL_BPS) revert InvalidAllocation();
        
        charityInfo[charityAddress] = CharityInfo({
            name: name,
            ein: ein,
            allocationBps: allocationBps,
            active: true
        });
        
        registeredCharities.push(charityAddress);
        
        emit CharityRegistered(charityAddress, name, ein, allocationBps);
    }
    
    /**
     * @notice Create a new distribution epoch
     * @param merkleRoot Root of the Merkle tree for this epoch's distributions
     * @dev Can only be called after DISTRIBUTION_INTERVAL has passed
     */
    function createEpoch(bytes32 merkleRoot) external onlyRootUpdater {
        if (block.timestamp < lastDistributionTime + DISTRIBUTION_INTERVAL) {
            revert TooEarlyForDistribution();
        }
        
        // Finalize previous epoch if exists
        if (currentEpoch > 0 && !epochs[currentEpoch].finalized) {
            _finalizeEpoch(currentEpoch);
        }
        
        currentEpoch++;
        
        uint256 ethBalance = address(this).balance;
        
        epochs[currentEpoch] = Epoch({
            merkleRoot: merkleRoot,
            totalAmount: ethBalance,
            distributedAmount: 0,
            startTime: block.timestamp,
            endTime: 0,
            finalized: false
        });
        
        lastDistributionTime = block.timestamp;
        
        emit EpochCreated(currentEpoch, merkleRoot, ethBalance, block.timestamp);
    }
    
    /**
     * @notice Claim funds for a charity using Merkle proof
     * @param epochNumber The epoch to claim from
     * @param charityAddress The charity claiming funds
     * @param amount Amount to claim
     * @param merkleProof Proof of inclusion in the Merkle tree
     */
    function claim(
        uint256 epochNumber,
        address charityAddress,
        uint256 amount,
        bytes32[] calldata merkleProof
    ) external nonReentrant {
        if (epochNumber == 0 || epochNumber > currentEpoch) revert EpochNotActive();
        if (claimed[epochNumber][charityAddress]) revert AlreadyClaimed();
        
        Epoch storage epoch = epochs[epochNumber];
        if (epoch.finalized) revert EpochNotActive();
        
        // Verify Merkle proof
        bytes32 leaf = keccak256(abi.encodePacked(charityAddress, amount));
        if (!MerkleProof.verify(merkleProof, epoch.merkleRoot, leaf)) {
            revert InvalidProof();
        }
        
        // Mark as claimed
        claimed[epochNumber][charityAddress] = true;
        epoch.distributedAmount += amount;
        totalEthDistributed += amount;
        
        // Transfer ETH to charity
        (bool success, ) = charityAddress.call{value: amount}("");
        require(success, "ETH transfer failed");
        
        emit FundsClaimed(epochNumber, charityAddress, amount, address(0));
    }
    
    /**
     * @notice Claim ERC20 tokens for a charity using Merkle proof
     * @param token ERC20 token address
     * @param epochNumber The epoch to claim from
     * @param charityAddress The charity claiming funds
     * @param amount Amount to claim
     * @param merkleProof Proof of inclusion in the Merkle tree
     */
    function claimToken(
        address token,
        uint256 epochNumber,
        address charityAddress,
        uint256 amount,
        bytes32[] calldata merkleProof
    ) external nonReentrant {
        if (token == address(0)) revert ZeroAddress();
        if (epochNumber == 0 || epochNumber > currentEpoch) revert EpochNotActive();
        if (tokenClaimed[epochNumber][token][charityAddress]) revert AlreadyClaimed();
        
        Epoch storage epoch = epochs[epochNumber];
        if (epoch.finalized) revert EpochNotActive();
        
        // Verify Merkle proof (includes token address)
        bytes32 leaf = keccak256(abi.encodePacked(token, charityAddress, amount));
        if (!MerkleProof.verify(merkleProof, epoch.merkleRoot, leaf)) {
            revert InvalidProof();
        }
        
        // Mark as claimed
        tokenClaimed[epochNumber][token][charityAddress] = true;
        totalTokenDistributed[token] += amount;
        
        // Transfer tokens to charity
        IERC20(token).safeTransfer(charityAddress, amount);
        
        emit FundsClaimed(epochNumber, charityAddress, amount, token);
    }
    
    /**
     * @notice Finalize an epoch (can be called by anyone after epoch ends)
     * @param epochNumber Epoch to finalize
     */
    function finalizeEpoch(uint256 epochNumber) external {
        _finalizeEpoch(epochNumber);
    }

    // ============ View Functions ============
    
    /**
     * @notice Get the number of registered charities
     * @return Number of charities
     */
    function getCharityCount() external view returns (uint256) {
        return registeredCharities.length;
    }
    
    /**
     * @notice Get all registered charity addresses
     * @return Array of charity addresses
     */
    function getAllCharities() external view returns (address[] memory) {
        return registeredCharities;
    }
    
    /**
     * @notice Check if a charity has claimed for an epoch
     * @param epochNumber Epoch number
     * @param charityAddress Charity address
     * @return True if claimed
     */
    function hasClaimed(uint256 epochNumber, address charityAddress) external view returns (bool) {
        return claimed[epochNumber][charityAddress];
    }
    
    /**
     * @notice Check if a charity has claimed tokens for an epoch
     * @param epochNumber Epoch number
     * @param token Token address
     * @param charityAddress Charity address
     * @return True if claimed
     */
    function hasClaimedToken(uint256 epochNumber, address token, address charityAddress) external view returns (bool) {
        return tokenClaimed[epochNumber][token][charityAddress];
    }
    
    /**
     * @notice Get epoch details
     * @param epochNumber Epoch to query
     * @return merkleRoot The Merkle root
     * @return totalAmount Total amount in epoch
     * @return distributedAmount Amount already distributed
     * @return startTime When epoch started
     * @return finalized Whether epoch is finalized
     */
    function getEpochInfo(uint256 epochNumber) external view returns (
        bytes32 merkleRoot,
        uint256 totalAmount,
        uint256 distributedAmount,
        uint256 startTime,
        bool finalized
    ) {
        Epoch storage epoch = epochs[epochNumber];
        return (
            epoch.merkleRoot,
            epoch.totalAmount,
            epoch.distributedAmount,
            epoch.startTime,
            epoch.finalized
        );
    }
    
    /**
     * @notice Calculate time until next distribution is allowed
     * @return Seconds until next distribution (0 if allowed now)
     */
    function timeUntilNextDistribution() external view returns (uint256) {
        uint256 nextTime = lastDistributionTime + DISTRIBUTION_INTERVAL;
        if (block.timestamp >= nextTime) return 0;
        return nextTime - block.timestamp;
    }
    
    /**
     * @notice Get current treasury balance
     * @return ETH balance available for distribution
     */
    function getTreasuryBalance() external view returns (uint256) {
        return address(this).balance;
    }

    // ============ Internal Functions ============
    
    function _finalizeEpoch(uint256 epochNumber) internal {
        Epoch storage epoch = epochs[epochNumber];
        if (epoch.finalized) return;
        
        epoch.finalized = true;
        epoch.endTime = block.timestamp;
        
        emit EpochFinalized(epochNumber, epoch.distributedAmount);
    }
}
