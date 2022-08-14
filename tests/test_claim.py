import brownie
from brownie import a, PacGovFungible


def test_token_payable(token, accounts):
    accounts[0].transfer(token, 10 ** 18)


def test_claim_eth_from_token(token, accounts):
    accounts[0].transfer(token, 10 ** 18)
    owner = accounts.at(token.owner(), force=True)
    init_bal = owner.balance()
    token.claim({"from": a[0]})
    assert owner.balance() == init_bal + 10 ** 18


def test_only_owner_can_claim_erc20(token, accounts, dummy_token):
    dummy_token.mint(token, 10 ** 18, {"from": dummy_token.owner()})
    with brownie.reverts("Only owner"):
        dummy_token.claim_erc20(dummy_token, {"from": accounts[1]})


def test_claim_erc20_from_token(token, accounts, dummy_token):
    dummy_token.mint(token, 10 ** 18, {"from": dummy_token.owner()})
    assert dummy_token.balanceOf(token) == 10 ** 18
    assert dummy_token.balanceOf(token.owner()) == 0

    token.claim_erc20(dummy_token, {"from": token.owner()})
    assert dummy_token.balanceOf(token) == 0
    assert dummy_token.balanceOf(token.owner()) == 10 ** 18


def test_bridge_payable(minter, accounts):
    accounts[0].transfer(minter, 10 ** 18)


def test_claim_eth_from_bridge(minter, token, accounts):
    accounts[0].transfer(minter, 10 ** 18)
    token.claim({"from": accounts[0]})

    owner = accounts.at(token.owner(), force=True)
    init_bal = owner.balance()

    minter.withdraw_eth({"from": accounts[0]})
    token.claim({"from": accounts[0]})
    assert owner.balance() == init_bal + 10 ** 18


def test_claim_erc20_from_bridge(minter, token, accounts, dummy_token):
    assert dummy_token.balanceOf(minter) == 0
    assert dummy_token.balanceOf(token) == 0

    dummy_token.mint(minter, 10 ** 18, {"from": dummy_token.owner()})
    assert dummy_token.balanceOf(minter) == 10 ** 18
    minter.withdraw_erc20(dummy_token, 10 ** 18, {"from": accounts[0]})

    assert dummy_token.balanceOf(minter) == 0
    assert dummy_token.balanceOf(token) == 10 ** 18


def test_gnosis_can_claim_eth():
    # Need a test to see if a Gnosis safe can claim raw ETH, which has been a problem before
    pass
