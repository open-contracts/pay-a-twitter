# Pay a Twitter account


This one's pretty simple. It allows you to pay $ETH to a Twitter account, even if the account owner doesn't have an Ethereum address yet.
Why is this useful? Because it allows you to make a take-it-or-leave-it offer to basically anyone. For example, we use this for the [Reforestation-Commitments](https://dapp.opencontracts.io/#/open-contracts/reforestation-commitments) contract, allowing anyone to commit funds to a pool which rewards the Brazilian Government if they reforest the rainforest in Brazil.

By calling the `deposit` function, users or contracts can deposit funds into the contract, declaring which `twitterHandle` is allowed to claim the funds. To do so, the account owner would call the `claim` function, which starts an interactive enclave session in which the owner proves they control the account by simply logging in and navigating to the "Account Details" page.

If you have the [MetaMask Wallet](https://metamask.io/) as browser plugin or mobile app, you can [play around with the contract](https://dapp.opencontracts.io/#/open-contracts/pay-a-twitter-account) on Ethereum's Ropsten Testnet! Just make sure your wallet is loaded with some free [Testnet ETH](https://faucet.egorfine.com/). It's also on [Optimistic Ethereum](https://optimism.io)'s Mainnet, which you can add to your Metamask wallet [here](https://chainlist.org/).
