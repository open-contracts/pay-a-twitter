pragma solidity ^0.8.0;

import "https://github.com/open-contracts/protocol/blob/main/solidity_contracts/OpenContractRopsten.sol";

contract PayATwitterAccount is OpenContract {
    
    mapping(string => uint256) balances;
    
    constructor () {
        setOracle("any", this.claim.selector);
    }
    
    function claim(bytes32 oracleID, string memory twitterHandle, address account)
    public checkOracle(oracleID, this.claim.selector) {
        uint256 balance = balances[twitterHandle];
        balances[twitterHandle] = 0;
        payable(account).transfer(balance);
    }

    function deposit(string memory twitterHandle) public payable {
        balances[twitterHandle] += msg.value;
    }
}
