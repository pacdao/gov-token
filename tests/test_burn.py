import brownie
from brownie import ZERO_ADDRESS


def test_burn_removes_tokens(token, v2_hodler):
    token.burn(token.balanceOf(v2_hodler), {"from": v2_hodler})
    assert token.balanceOf(v2_hodler) == 0


def test_cannot_burn_more_than_balance(token, v2_hodler):
    with brownie.reverts():
        token.burn(token.balanceOf(v2_hodler) + 1, {"from": v2_hodler})


def test_burn_updates_total_supply(token, v2_hodler):
    user_bal = token.balanceOf(v2_hodler)
    init_supply = token.totalSupply()

    token.burn(user_bal, {"from": v2_hodler})
    assert token.totalSupply() == init_supply - user_bal


def test_zero_addr_transfer_updates_total_supply(token, v2_hodler):
    user_bal = token.balanceOf(v2_hodler)
    init_supply = token.totalSupply()

    token.transfer(ZERO_ADDRESS, user_bal, {"from": v2_hodler})
    assert token.totalSupply() == init_supply - user_bal
