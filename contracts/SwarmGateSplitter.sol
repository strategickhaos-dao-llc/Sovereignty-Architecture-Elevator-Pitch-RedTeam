// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title SwarmGateSplitter
 * @dev A contract that splits incoming ETH payments with 7% going to charity
 * and 93% going to operations. Charity funds are accumulated and can be
 * distributed evenly among registered charity addresses.
 * 
 * Note: The distribute() function is intentionally public to allow anyone
 * to trigger charity distributions, promoting transparency and community involvement.
 */
contract SwarmGateSplitter {
    /// @notice Charity allocation in basis points (700 = 7%)
    uint256 public constant CHARITY_BPS = 700;

    /// @notice Operations wallet address that receives 93% of incoming funds
    address payable public immutable OPS;

    /// @notice Array of charity addresses that receive distributed funds
    address payable[] public charities;

    /// @notice Emitted when funds are received and split
    event FundsReceived(address indexed sender, uint256 amount, uint256 toOps, uint256 toCharity);

    /// @notice Emitted when charity funds are distributed
    event CharityDistributed(uint256 totalAmount, uint256 perCharity, uint256 remainder);

    /**
     * @dev Constructor sets the operations wallet and charity addresses
     * @param o Operations wallet address (must not be zero address)
     * @param c Array of charity wallet addresses (must not be empty)
     */
    constructor(address payable o, address payable[] memory c) {
        require(o != address(0), "OPS address cannot be zero");
        require(c.length > 0, "Must have at least one charity");
        OPS = o;
        charities = c;
    }

    /**
     * @dev Receive function that splits incoming ETH
     * 7% is kept for charity distribution, 93% goes to operations
     */
    receive() external payable {
        uint256 toCharity = msg.value * CHARITY_BPS / 10000;
        uint256 toOps = msg.value - toCharity;

        (bool success, ) = OPS.call{value: toOps}("");
        require(success, "OPS transfer failed");

        emit FundsReceived(msg.sender, msg.value, toOps, toCharity);
    }

    /**
     * @dev Distributes accumulated charity funds evenly among all charity addresses
     * Any remainder from integer division stays in the contract for the next distribution
     */
    function distribute() external {
        uint256 bal = address(this).balance;
        require(bal > 0, "No balance to distribute");

        uint256 each = bal / charities.length;
        uint256 remainder = bal % charities.length;

        for (uint256 i = 0; i < charities.length; i++) {
            (bool success, ) = charities[i].call{value: each}("");
            require(success, "Charity transfer failed");
        }

        emit CharityDistributed(bal, each, remainder);
    }

    /**
     * @dev Returns the number of registered charities
     */
    function getCharitiesCount() external view returns (uint256) {
        return charities.length;
    }

    /**
     * @dev Returns all charity addresses
     */
    function getCharities() external view returns (address payable[] memory) {
        return charities;
    }
}
