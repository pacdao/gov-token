import brownie
from brownie import ZERO_ADDRESS, accounts


def test_no_upgrade_without_approval(token, v1_token, v1_hodler_addr, minter):
    assert v1_token.allowance(v1_hodler_addr, token) == 0
    with brownie.reverts():
        minter.upgrade(v1_hodler_addr, {"from": v1_hodler_addr})


def test_initial_balance_empty(token, v1_hodler):
    assert token.balanceOf(v1_hodler) == 0


def test_holders_of_v1_can_upgrade(token, v1_token, v1_hodler, minter):
    minter.upgrade(v1_hodler, {"from": v1_hodler})
    assert token.balanceOf(v1_hodler) > 0


def test_holders_of_v1_can_be_upgraded_by_anybody(token, v1_token, v1_hodler, minter):
    minter.upgrade(v1_hodler, {"from": accounts[0]})
    assert token.balanceOf(v1_hodler) > 0


def test_non_hodler_of_v1_cannot_upgrade(token, v1_token, minter):
    assert token.balanceOf(accounts[1]) == 0
    with brownie.reverts():
        minter.upgrade(accounts[0], {"from": accounts[0]})
    assert token.balanceOf(accounts[1]) == 0


def test_upgrading_kills_v1_stake(token, v1_hodler, v1_token, minter):
    minter.upgrade(v1_hodler, {"from": v1_hodler})
    assert v1_token.balanceOf(v1_hodler) == 0


def test_cannot_upgrade_twice(token, v1_hodler, v1_token, minter):
    minter.upgrade(v1_hodler, {"from": v1_hodler})
    with brownie.reverts():
        minter.upgrade(v1_hodler, {"from": v1_hodler})


def test_can_update_new_minter_addr(token):
    token.update_minter(accounts[0], {"from": token.owner()})
    assert token.minter() == accounts[0]


def test_nonowner_cannot_update_minter(token):
    assert accounts[0] != token.owner()
    with brownie.reverts("Only owner"):
        token.update_minter(accounts[0], {"from": accounts[0]})


def test_can_revoke_minter_addr(token):
    new_minter = ZERO_ADDRESS
    token.update_minter(new_minter, {"from": token.owner()})
    assert token.minter() == new_minter


def test_new_minter_can_mint(token):
    new_minter = accounts[0]
    token.update_minter(new_minter, {"from": token.owner()})
    assert token.minter() == new_minter

    init_bal = token.balanceOf(accounts[0])
    token.mint(accounts[0], 10**18, {"from": new_minter})

    assert token.balanceOf(accounts[0]) == init_bal + 10**18


def test_cannot_mint_after_minter_addr_revoked(token):
    new_minter = accounts[0]
    token.update_minter(new_minter, {"from": token.owner()})
    assert token.minter() == new_minter

    token.update_minter(accounts[1], {"from": token.owner()})
    assert token.minter() == accounts[1]

    with brownie.reverts():
        token.mint(accounts[0], 10**18, {"from": new_minter})


def test_cannot_mint_from_random_addr(token, accounts):
    assert token.owner() != accounts[0]
    with brownie.reverts():
        token.mint(accounts[0], 10 ** 18, {'from': accounts[0]})
