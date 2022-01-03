pragma solidity ^0.8.0;

import "https://github.com/open-contracts/protocol/blob/main/solidity_contracts/OpenContractRopsten.sol";

contract PayTwitterAccount is OpenContractAlpha {
    
    mapping(string => bool) owner;
    
    constructor (string memory twitterHandle) {
        owner[twitterHandle] = true;
    }
    
    function claim(bytes32 oracleHash, string memory twitterHandle, address tweetedAddress, address erc20address)
    public _oracle(oracleHash, msgSender, this.claim.selector) {
        require(owner[twitterHandle], "Tweet does not come from the correct twitter handle.");
        
        // transfer all ETH
        payable(tweetedAddress).transfer(address(this).balance);
        
        // transfer all the contracts ERC20 
        IERC20 token = IERC20(erc20address);
        token.transfer(tweetedAddress, token.balanceOf(address(this)));
    }
}

interface IERC20 {
    function transfer(address recipient, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}
