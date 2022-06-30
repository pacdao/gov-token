import brownie
from brownie import accounts


def test_initial_balance_empty(token, v1_hodler):
    assert token.balanceOf(v1_hodler) == 0


def test_cannot_upgrade_without_approval(token, v1_hodler, v1_token):
    v1_token.approve(token, 0, {"from": v1_hodler})
    with brownie.reverts("No Approval"):
        token.upgrade(v1_hodler, {"from": v1_hodler})


def test_holders_of_v1_can_upgrade(token, v1_token, v1_hodler):
    token.upgrade(v1_hodler, {"from": v1_hodler})
    assert token.balanceOf(v1_hodler) > 0


def test_holders_of_v1_can_be_upgraded_by_anybody(token, v1_token, v1_hodler):
    token.upgrade(v1_hodler, {"from": accounts[0]})
    assert token.balanceOf(v1_hodler) > 0


def test_non_hodler_of_v1_cannot_upgrade(token, v1_token):
    assert token.balanceOf(accounts[1]) == 0
    with brownie.reverts("No balance"):
        token.upgrade(accounts[0], {"from": accounts[0]})
    assert token.balanceOf(accounts[1]) == 0


def test_upgrading_kills_v1_stake(token, v1_hodler, v1_token):
    token.upgrade(v1_hodler, {"from": v1_hodler})
    assert v1_token.balanceOf(v1_hodler) == 0


def test_cannot_upgrade_twice(token, v1_hodler, v1_token):
    token.upgrade(v1_hodler, {"from": v1_hodler})
    with brownie.reverts("No balance"):
        token.upgrade(v1_hodler, {"from": v1_hodler})

