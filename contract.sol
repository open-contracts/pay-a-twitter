pragma solidity ^0.8.0;

import "https://github.com/open-contracts/protocol/blob/main/solidity_contracts/OpenContractRopsten.sol";

contract FiatSwap is OpenContractAlpha {

    mapping(bytes32 => address) beneficiary;
    mapping(bytes32 => uint256) amount;


    function EthForHash(bytes32 txHash) public view returns(uint256) {
        require(msg.sender == beneficiary[txHash], "No Eth offered for you.");
        return amount[txHash];
    }


    function computeHash(string memory sellerVenmo, uint256 priceInCent, string memory transactionMessage, string memory secret) public pure returns(bytes32) {
        return keccak256(abi.encodePacked(sellerVenmo, priceInCent, transactionMessage, secret));
    }

    function venmoPurchase(bytes32 oracleHash, address payable msgSender, bytes32 txHash) 
    public _oracle(oracleHash, msgSender, this.venmoPurchase.selector) returns(bool) {
        require(beneficiary[txHash] == msgSender);
        uint256 reward = amount[txHash];
        amount[txHash] = 0;
        return msgSender.send(reward);
    }

    function sell(address buyer, bytes32 txHash) public payable {
        amount[txHash] = msg.value;
        beneficiary[txHash] = buyer;
    }
}
