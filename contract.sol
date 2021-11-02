pragma solidity ^0.8.0;

import "https://github.com/open-contracts/protocol/blob/main/solidity_contracts/OpenContractRopsten.sol";

contract FiatSwap is OpenContractAlpha {
    
    mapping(bytes32 => address) seller;
    mapping(bytes32 => address) buyer;
    mapping(bytes32 => uint256) amount;
    mapping(bytes32 => uint256) lockedUntil;


    function secondsLeft(bytes32 offerHash) public view returns(int256) {
        return int256(lockedUntil[offerHash]) - int256(block.timestamp);
    }

    function ethOffered(bytes32 offerHash) public view returns(uint256) {
        require(msg.sender == buyer[offerHash], "No ETH offered for you.");
        return amount[offerHash];
    }


    function computeHash(string memory sellerVenmo, uint256 priceInCent, string memory transactionMessage, string memory secret) public pure returns(bytes32) {
        return keccak256(abi.encodePacked(sellerVenmo, priceInCent, transactionMessage, secret));
    }

    function venmoPurchase(bytes32 oracleHash, address payable msgSender, bytes32 offerHash) 
    public _oracle(oracleHash, msgSender, this.venmoPurchase.selector) returns(bool) {
        require(buyer[offerHash] == msgSender);
        uint256 payment = amount[offerHash];
        amount[offerHash] = 0;
        return msgSender.send(payment);
    }

    function offer(address to, bytes32 offerHash, uint256 lockForSeconds) public payable {
        amount[offerHash] = msg.value;
        buyer[offerHash] = to;
        lockedUntil[offerHash] = block.timestamp + lockForSeconds;
        seller[offerHash] = msg.sender;
    }
    
    function retract(bytes32 offerHash) public returns(bool) {
        require(seller[offerHash] == msg.sender, 'only seller can retract offer');
        uint256 payment = amount[offerHash];
        amount[offerHash] = 0;
        return payable(msg.sender).send(payment);
    }
}
