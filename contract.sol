pragma solidity ^0.8.0;
import "https://github.com/open-contracts/protocol/blob/main/solidity_contracts/OpenContractRopsten.sol";

contract PayATwitterAccount is OpenContract {
    
    mapping(string => uint256) public balances;
    
    constructor () {
        setOracleHash(this.claim.selector, 0x18397129c99c63baae375f7b480aa97f2fcf1d747b171b7db033c788fd732098);
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
