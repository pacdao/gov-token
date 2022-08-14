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

def test_mint_many_mints_many(accounts, token, owner):
    list1 = []
    list2 = []
    for i in range(8):
        list1.append(accounts[i + 1])
        list2.append(100)
    token.mint_many(list1, list2, {"from": owner})
    for i in range(8):
        assert token.balanceOf(accounts[i + 1]) == 100


def test_partial_mint_many_mints_many(accounts, token, owner):
    list1 = []
    list2 = []
    for i in range(6):
        list1.append(accounts[i + 1])
        list2.append(100)
    list1.append(ZERO_ADDRESS)
    list1.append(ZERO_ADDRESS)
    list2.append(0)
    list2.append(0)
    token.mint_many(list1, list2, {"from": owner})
    for i in range(6):
        assert token.balanceOf(accounts[i + 1]) == 100


def test_mint_increases_supply(accounts, token, owner):
    init = token.totalSupply()
    token.mint(accounts[2], 1000, {"from": owner})
    assert token.totalSupply() == 1000 + init


def test_mint_many_increases_supply(accounts, token, owner):
    init = token.totalSupply()

    list1 = []
    list2 = []
    run_tot = 0
    for i in range(8):
        list1.append(accounts[i + 1])
        amount = 100 * 10**18 * i
        list2.append(amount)
        run_tot += amount

    token.mint_many(list1, list2, {"from": owner})

    assert token.totalSupply() == run_tot + init


def test_mint_event_fires(accounts, token, owner):
    tx = token.mint(accounts[2], 1000, {"from": owner})
    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [ZERO_ADDRESS, accounts[2], 1000]


def test_mint_many_events_fire(accounts, token, owner):
    tx = token.mint_many(accounts[0:8], [1000] * 8, {"from": owner})

    assert len(tx.events) == 8


def test_cannot_mint_to_zero_addr(token, owner):
    init_supply = token.totalSupply()
    tx = token.mint(ZERO_ADDRESS, 1000, {"from": owner})
    assert len(tx.events) == 0
    assert token.totalSupply() == init_supply


def test_cannot_mint_many_to_zero_addrs(token, owner):
    init_supply = token.totalSupply()
    tx = token.mint_many([ZERO_ADDRESS] * 8, [1000] * 8, {"from": owner})
    assert len(tx.events) == 0
    assert token.totalSupply() == init_supply
