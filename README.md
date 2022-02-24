# PAC DAO GOVERNANCE TOKEN

![PAC DAO](https://cdn.substack.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F23ecc600-c85b-4438-8bc2-5dadfdf7aeb4_700x405.png)

A governance token for [PAC DAO](https://pac.xyz).

The token is a vanilla ERC20 token with the following adjustments.

 * Has an owner with sole minting power (the DAO treasury multisig)
 * Transfers to anybody (except owner address) are disabled
 * Owner can set new owner
 * Mint Many function

Token is non-transferrable and therefore not tradable, simply a ledger to allow for governance voting in PAC DAO.  The full announcement [was made here](https://pacdao.substack.com/p/pac-governance-token).  If you are interested in earning the token please join the Discord. 

View the Governance Token on Etherscan at [0x3459cfce9c0306eb1d5d0e2b78144c9fbd94c87b](https://etherscan.io/address/0x3459cfce9c0306eb1d5d0e2b78144c9fbd94c87b)

* [🌐  Web](https://pac.xyz/)
* [🎮  Discord ](https://discord.gg/tbBKXQqm)
* [🛫  Telegram ](https://t.me/joinchat/VYYqN19O3Wc4OTZh)
* [🦅  Twitter](https://twitter.com/pacdao)

---

## Instructions
Based on the [Vyper Token Mix](https://github.com/brownie-mix/vyper-token-mix)

A bare-bones implementation of the Ethereum [ERC-20 standard](https://eips.ethereum.org/EIPS/eip-20), written in [Vyper](https://github.com/vyperlang/vyper).

For [Solidity](https://github.com/ethereum/solidity), check out [`token-mix`](https://github.com/brownie-mix/token-mix).

## Installation

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), if you haven't already.

2. Download the mix.

    ```bash
    brownie bake vyper-token
    ```

## Basic Use

This mix provides a [simple template](contracts/Token.vy) upon which you can build your own token, as well as unit tests providing 100% coverage for core ERC20 functionality.

To interact with a deployed contract in a local environment, start by opening the console:

```bash
brownie console
```

Next, deploy a test token:

```python
>>> token = Token.deploy("Test Token", "TST", 18, 1e21, {'from': accounts[0]})

Transaction sent: 0x4a61edfaaa8ba55573603abd35403cf41291eca443c983f85de06e0b119da377
  Gas price: 0.0 gwei   Gas limit: 12000000
  Token.constructor confirmed - Block: 1   Gas used: 521513 (4.35%)
  Token deployed at: 0xd495633B90a237de510B4375c442C0469D3C161C
```

You now have a token contract deployed, with a balance of `1e21` assigned to `accounts[0]`:

```python
>>> token
<Token Contract '0xd495633B90a237de510B4375c442C0469D3C161C'>

>>> token.balanceOf(accounts[0])
1000000000000000000000

>>> token.transfer(accounts[1], 1e18, {'from': accounts[0]})
Transaction sent: 0xb94b219148501a269020158320d543946a4e7b9fac294b17164252a13dce9534
  Gas price: 0.0 gwei   Gas limit: 12000000
  Token.transfer confirmed - Block: 2   Gas used: 51668 (0.43%)

<Transaction '0xb94b219148501a269020158320d543946a4e7b9fac294b17164252a13dce9534'>
```

## Testing

To run the tests:

```bash
brownie test
```

The unit tests included in this mix are very generic and should work with any ERC20 compliant smart contract. To use them in your own project, all you must do is modify the deployment logic in the [`tests/conftest.py::token`](tests/conftest.py) fixture.

## Resources

To get started with Brownie:

* Check out the other [Brownie mixes](https://github.com/brownie-mix/) that can be used as a starting point for your own contracts. They also provide example code to help you get started.
* ["Getting Started with Brownie"](https://medium.com/@iamdefinitelyahuman/getting-started-with-brownie-part-1-9b2181f4cb99) is a good tutorial to help you familiarize yourself with Brownie.
* For more in-depth information, read the [Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/).


Any questions? Join our [Gitter](https://gitter.im/eth-brownie/community) channel to chat and share with others in the community.

## License

This project is licensed under the [MIT license](LICENSE).
