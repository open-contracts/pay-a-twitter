pragma solidity ^0.8.0;

import "https://github.com/open-contracts/protocol/blob/main/solidity_contracts/OpenContractRopsten.sol";

contract PayTwitterAccount is OpenContractAlpha {
    
    mapping(string => bool) owner;
    
    constructor (string memory twitterHandle) {
        owner[twitterHandle] = true;
        setOracle("any", this.claim.selector)
    }
    
    function claim(bytes32 oracleID, string memory twitterHandle, address tweetedAddress)
    public checkOracle(oracleID, this.claim.selector) {
        require(owner[twitterHandle], "Tweet does not come from the correct twitter handle.");
        
        // transfer all ETH
        payable(tweetedAddress).transfer(address(this).balance);
    }
}
