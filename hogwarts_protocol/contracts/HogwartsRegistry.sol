// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title HogwartsRegistry
 * @author Strategickhaos DAO LLC / Valoryield Engine
 * @notice The Great Hall Ledger - On-chain registry for educational artifacts (Spells)
 * @dev Implements ERC721 with soulbound characteristics for credential verification
 * 
 * This contract serves as the "proof layer" for the Hogwarts Protocol:
 * - Registers verified spells (educational work) as NFTs
 * - Stores content hashes for integrity verification
 * - Links to course/assignment metadata
 * - Supports soulbound mode (non-transferable) for credentials
 */
contract HogwartsRegistry is ERC721, ERC721URIStorage, AccessControl {
    using Counters for Counters.Counter;

    // ============================================
    // ROLES
    // ============================================
    bytes32 public constant VERIFIER_ROLE = keccak256("VERIFIER_ROLE");
    bytes32 public constant PLATFORM_ROLE = keccak256("PLATFORM_ROLE");

    // ============================================
    // STATE
    // ============================================
    Counters.Counter private _tokenIdCounter;
    
    // Soulbound mode - when true, tokens cannot be transferred
    bool public soulboundMode;
    
    // Platform identifier
    string public constant PLATFORM_NAME = "CourseQuest Hogwarts";
    string public constant PLATFORM_VERSION = "1.0.0";
    
    // ============================================
    // STRUCTS
    // ============================================
    
    /**
     * @notice On-chain spell record
     * @param owner Wallet address of the spell creator
     * @param contentHash SHA-256 hash of the spell content
     * @param courseCode Course identifier (e.g., "MAT-243")
     * @param assignmentCode Assignment identifier (e.g., "P1")
     * @param grade Grade received (e.g., "B+")
     * @param institution Educational institution (e.g., "SNHU")
     * @param verifiedAt Timestamp of verification
     * @param offChainId Reference to off-chain database ID
     */
    struct SpellRecord {
        address owner;
        bytes32 contentHash;
        string courseCode;
        string assignmentCode;
        string grade;
        string institution;
        uint256 verifiedAt;
        string offChainId;
    }
    
    // Token ID => Spell Record
    mapping(uint256 => SpellRecord) public spells;
    
    // Content hash => Token ID (for uniqueness check)
    mapping(bytes32 => uint256) public contentHashToToken;
    
    // Owner => Token IDs (for enumeration)
    mapping(address => uint256[]) private _ownerTokens;

    // ============================================
    // EVENTS
    // ============================================
    
    /**
     * @notice Emitted when a new spell is registered
     */
    event SpellRegistered(
        uint256 indexed tokenId,
        address indexed owner,
        bytes32 contentHash,
        string courseCode,
        string grade
    );
    
    /**
     * @notice Emitted when soulbound mode is toggled
     */
    event SoulboundModeChanged(bool enabled);
    
    /**
     * @notice Emitted when spell metadata is updated
     */
    event SpellMetadataUpdated(uint256 indexed tokenId, string newURI);

    // ============================================
    // CONSTRUCTOR
    // ============================================
    
    /**
     * @notice Initialize the Hogwarts Registry
     * @param _soulboundMode Whether tokens should be non-transferable
     */
    constructor(bool _soulboundMode) ERC721("Hogwarts Spell Registry", "SPELL") {
        soulboundMode = _soulboundMode;
        
        // Grant admin role to deployer
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(VERIFIER_ROLE, msg.sender);
        _grantRole(PLATFORM_ROLE, msg.sender);
    }

    // ============================================
    // REGISTRATION FUNCTIONS
    // ============================================
    
    /**
     * @notice Register a verified spell on-chain
     * @param _to Wallet address of the spell owner
     * @param _contentHash SHA-256 hash of the spell content
     * @param _courseCode Course identifier
     * @param _assignmentCode Assignment identifier
     * @param _grade Grade received
     * @param _institution Educational institution
     * @param _offChainId Reference to off-chain database
     * @param _tokenURI Metadata URI
     * @return tokenId The ID of the newly minted spell NFT
     */
    function registerSpell(
        address _to,
        bytes32 _contentHash,
        string calldata _courseCode,
        string calldata _assignmentCode,
        string calldata _grade,
        string calldata _institution,
        string calldata _offChainId,
        string calldata _tokenURI
    ) external onlyRole(VERIFIER_ROLE) returns (uint256) {
        // Ensure content hash is unique (no duplicate submissions)
        require(contentHashToToken[_contentHash] == 0, "Spell already registered");
        require(_contentHash != bytes32(0), "Invalid content hash");
        
        // Mint the spell NFT
        _tokenIdCounter.increment();
        uint256 tokenId = _tokenIdCounter.current();
        
        _safeMint(_to, tokenId);
        _setTokenURI(tokenId, _tokenURI);
        
        // Store spell record
        spells[tokenId] = SpellRecord({
            owner: _to,
            contentHash: _contentHash,
            courseCode: _courseCode,
            assignmentCode: _assignmentCode,
            grade: _grade,
            institution: _institution,
            verifiedAt: block.timestamp,
            offChainId: _offChainId
        });
        
        // Index content hash
        contentHashToToken[_contentHash] = tokenId;
        
        // Track owner tokens
        _ownerTokens[_to].push(tokenId);
        
        emit SpellRegistered(tokenId, _to, _contentHash, _courseCode, _grade);
        
        return tokenId;
    }
    
    /**
     * @notice Batch register multiple spells
     * @dev Gas optimization for bulk registrations
     */
    function batchRegisterSpells(
        address[] calldata _owners,
        bytes32[] calldata _contentHashes,
        string[] calldata _courseCodes,
        string[] calldata _assignmentCodes,
        string[] calldata _grades,
        string calldata _institution,
        string[] calldata _offChainIds,
        string[] calldata _tokenURIs
    ) external onlyRole(VERIFIER_ROLE) returns (uint256[] memory) {
        require(
            _owners.length == _contentHashes.length &&
            _owners.length == _courseCodes.length &&
            _owners.length == _grades.length &&
            _owners.length == _tokenURIs.length,
            "Array length mismatch"
        );
        
        uint256[] memory tokenIds = new uint256[](_owners.length);
        
        for (uint256 i = 0; i < _owners.length; i++) {
            require(contentHashToToken[_contentHashes[i]] == 0, "Duplicate content hash");
            
            _tokenIdCounter.increment();
            uint256 tokenId = _tokenIdCounter.current();
            
            _safeMint(_owners[i], tokenId);
            _setTokenURI(tokenId, _tokenURIs[i]);
            
            spells[tokenId] = SpellRecord({
                owner: _owners[i],
                contentHash: _contentHashes[i],
                courseCode: _courseCodes[i],
                assignmentCode: _assignmentCodes[i],
                grade: _grades[i],
                institution: _institution,
                verifiedAt: block.timestamp,
                offChainId: _offChainIds[i]
            });
            
            contentHashToToken[_contentHashes[i]] = tokenId;
            _ownerTokens[_owners[i]].push(tokenId);
            
            tokenIds[i] = tokenId;
            
            emit SpellRegistered(tokenId, _owners[i], _contentHashes[i], _courseCodes[i], _grades[i]);
        }
        
        return tokenIds;
    }

    // ============================================
    // QUERY FUNCTIONS
    // ============================================
    
    /**
     * @notice Get spell record by token ID
     */
    function getSpell(uint256 _tokenId) external view returns (SpellRecord memory) {
        require(ownerOf(_tokenId) != address(0), "Spell does not exist");
        return spells[_tokenId];
    }
    
    /**
     * @notice Get token ID by content hash
     */
    function getTokenByContentHash(bytes32 _contentHash) external view returns (uint256) {
        uint256 tokenId = contentHashToToken[_contentHash];
        require(tokenId != 0, "Spell not found");
        return tokenId;
    }
    
    /**
     * @notice Verify a spell exists with given content hash and owner
     */
    function verifySpell(bytes32 _contentHash, address _owner) external view returns (bool) {
        uint256 tokenId = contentHashToToken[_contentHash];
        if (tokenId == 0) return false;
        return ownerOf(tokenId) == _owner;
    }
    
    /**
     * @notice Get all token IDs owned by an address
     */
    function getOwnerTokens(address _owner) external view returns (uint256[] memory) {
        return _ownerTokens[_owner];
    }
    
    /**
     * @notice Get total number of registered spells
     */
    function totalSpells() external view returns (uint256) {
        return _tokenIdCounter.current();
    }

    // ============================================
    // ADMIN FUNCTIONS
    // ============================================
    
    /**
     * @notice Toggle soulbound mode
     * @dev When enabled, tokens cannot be transferred
     */
    function setSoulboundMode(bool _enabled) external onlyRole(DEFAULT_ADMIN_ROLE) {
        soulboundMode = _enabled;
        emit SoulboundModeChanged(_enabled);
    }
    
    /**
     * @notice Update spell metadata URI
     */
    function updateSpellMetadata(uint256 _tokenId, string calldata _newURI) 
        external 
        onlyRole(PLATFORM_ROLE) 
    {
        require(ownerOf(_tokenId) != address(0), "Spell does not exist");
        _setTokenURI(_tokenId, _newURI);
        emit SpellMetadataUpdated(_tokenId, _newURI);
    }
    
    /**
     * @notice Grant verifier role to an address
     */
    function addVerifier(address _verifier) external onlyRole(DEFAULT_ADMIN_ROLE) {
        grantRole(VERIFIER_ROLE, _verifier);
    }
    
    /**
     * @notice Revoke verifier role from an address
     */
    function removeVerifier(address _verifier) external onlyRole(DEFAULT_ADMIN_ROLE) {
        revokeRole(VERIFIER_ROLE, _verifier);
    }

    // ============================================
    // OVERRIDE FUNCTIONS
    // ============================================
    
    /**
     * @notice Override transfer to enforce soulbound mode
     */
    function _update(
        address to,
        uint256 tokenId,
        address auth
    ) internal override returns (address) {
        address from = _ownerOf(tokenId);
        
        // Allow minting (from == 0) and burning (to == 0) always
        // Block transfers if soulbound mode is enabled
        if (from != address(0) && to != address(0) && soulboundMode) {
            revert("Soulbound: token is non-transferable");
        }
        
        return super._update(to, tokenId, auth);
    }
    
    /**
     * @dev Required override for tokenURI
     */
    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
    
    /**
     * @dev Required override for supportsInterface
     */
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
