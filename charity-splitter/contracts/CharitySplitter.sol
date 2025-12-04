// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/Address.sol";

/**
 * @title CharitySplitter
 * @notice Irrevocable splitter: 93% to Ops, 7% to Charity Distributor.
 * @dev Uses a push-payment model on receipt.
 */
contract CharitySplitter {
    using Address for address payable;

    // The operations wallet (93%)
    address payable public immutable opsWallet;
    
    // The charity distributor contract (7%)
    address payable public immutable charityDistributor;

    event FundsReceived(address indexed sender, uint256 amount);
    event FundsSplit(uint256 opsAmount, uint256 charityAmount);

    constructor(address payable _opsWallet, address payable _charityDistributor) {
        require(_opsWallet != address(0), "Ops wallet cannot be zero");
        require(_charityDistributor != address(0), "Distributor cannot be zero");
        opsWallet = _opsWallet;
        charityDistributor = _charityDistributor;
    }

    /**
     * @notice Handles incoming payments and splits them immediately.
     * @dev Reverts if either transfer fails.
     */
    receive() external payable {
        emit FundsReceived(msg.sender, msg.value);
        _split(msg.value);
    }

    function _split(uint256 amount) internal {
        if (amount == 0) return;

        // Calculate 7% share
        uint256 charityShare = (amount * 7) / 100;
        uint256 opsShare = amount - charityShare;

        // Forward funds irrevocably
        // We use low-level call to prevent gas limit issues on receiving contracts
        (bool successOps, ) = opsWallet.call{value: opsShare}("");
        require(successOps, "Transfer to Ops failed");

        (bool successCharity, ) = charityDistributor.call{value: charityShare}("");
        require(successCharity, "Transfer to Charity failed");

        emit FundsSplit(opsShare, charityShare);
    }
}
