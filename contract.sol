pragma solidity ^0.8.0;
import "https://github.com/open-contracts/protocol/blob/main/solidity_contracts/OpenContractRopsten.sol";

contract PayATwitterAccount is OpenContract {
    
    mapping(string => uint256) public balances;
    
    constructor () {
        setOracleHash(this.claim.selector, 0x0cc49493cdc43d18101a186f18f0cf9dbc5dd346e424dcad8589172a69163748);
    }
    
    function claim(string memory twitterHandle, address tweetedAddress) public requiresOracle {
        uint256 balance = balances[twitterHandle];
        balances[twitterHandle] = 0;
        payable(tweetedAddress).transfer(balance);
    }

    function deposit(string memory twitterHandle) public payable {
        balances[twitterHandle] += msg.value;
    }
}
