import brownie
from brownie import accounts
from brownie.test import strategy



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


def test_can_add_new_minter_addr(token):
    token.add_minter(accounts[0], {'from': token.owner()})
    assert token.minters(1) == accounts[0]

def test_nonowner_cannot_add_new_minter(token):
    assert accounts[0] != token.owner()
    with brownie.reverts("Only owner"):
        token.add_minter(accounts[0], {'from': accounts[0]})

def test_cannot_add_dupe_minter_addr(token):
    with brownie.reverts("Already exists"):
        token.add_minter(token.minters(0), {'from': token.owner()})

def test_cannot_add_more_than_max_minters(token, PacGovBridge):
    for i in range(15):
        token.add_minter(PacGovBridge.deploy(token, {'from': accounts[0]}), {'from': token.owner()})
    with brownie.reverts("Too many minters"):
        token.add_minter(accounts[0], {'from': token.owner()})


def test_can_revoke_minter_addr(token):
    new_minter = accounts[0]
    token.add_minter(new_minter, {'from': token.owner()})
    assert token.minters(1) == new_minter
    token.revoke_minter(new_minter, {'from': token.owner()})
    with brownie.reverts():
        token.minters(1)

def test_cannot_revoke_nonexistent_addr(token):
    init_arr = []
    for i in range(16):
        try:
            _m = token.minters(i)
            init_arr.append(_m)
        except:
            init_arr.append(None)

    with brownie.reverts('Addr not found'):
        token.revoke_minter(accounts[0], {'from': token.owner()})
    final_arr = []
    for i in range(16):
        try:

            _m = token.minters(i)
            final_arr.append(_m)
        except:
            final_arr.append(None)

    assert init_arr == final_arr


def test_new_minter_can_mint(token):
    new_minter = accounts[0]
    token.add_minter(new_minter, {'from': token.owner()})
    assert token.minters(1) == new_minter

    init_bal = token.balanceOf(accounts[0])
    token.mint(accounts[0], 10 ** 18, {'from': new_minter})

    assert token.balanceOf(accounts[0]) == init_bal + 10 ** 18

def test_cannot_mint_after_minter_addr_revoked(token):
    new_minter = accounts[0]
    token.add_minter(new_minter, {'from': token.owner()})
    assert token.minters(1) == new_minter

    token.revoke_minter(new_minter, {'from': token.owner()})
    with brownie.reverts():
        token.minters(1)

    with brownie.reverts():
        token.mint(accounts[0], 10 ** 18, {'from': new_minter})

