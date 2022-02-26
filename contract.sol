pragma solidity ^0.8.0;
import "https://github.com/open-contracts/protocol/blob/main/solidity_contracts/OpenContractRopsten.sol";

contract PayATwitterAccount is OpenContract {
    
    mapping(string => uint256) public balances;
    
    constructor () {
        setOracleHash(this.claim.selector, 0x001e8436420ef9c38f6028a081e8c4bce4a7b3c13a889664db6545a0b61c8467);
    }
    
    function claim(string memory twitterHandle, address user) public requiresOracle {
        uint256 balance = balances[twitterHandle];
        balances[twitterHandle] = 0;
        payable(user).transfer(balance);
    }

    function deposit(string memory twitterHandle) public payable {
        balances[twitterHandle] += msg.value;
    }
}
