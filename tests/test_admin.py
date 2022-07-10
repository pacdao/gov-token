#!/usr/bin/python3
import brownie
from brownie import ZERO_ADDRESS


def test_owner_can_mint(accounts, token, owner):
    init_bal = token.balanceOf(accounts[1])
    token.mint(accounts[1], 100, {"from": owner})
    assert token.balanceOf(accounts[1]) == init_bal + 100


def test_nonowner_cannot_mint(accounts, token):
    with brownie.reverts("Only minters"):
        token.mint(accounts[1], 100, {"from": accounts[1]})


def test_can_transfer_to_owner(accounts, token, owner):
    token.mint(accounts[1], 100, {"from": owner})

    init_balance = token.balanceOf(owner)
    sender_balance = token.balanceOf(accounts[1])
    amount = sender_balance // 4
    assert amount > 0

    token.transfer(owner, amount, {"from": accounts[1]})
    assert token.balanceOf(owner) == init_balance + amount


def test_transfer_event_fires(accounts, token, owner):
    token.mint(accounts[1], 100, {"from": owner})
    amount = token.balanceOf(accounts[1])
    tx = token.transfer(owner, amount, {"from": accounts[1]})

    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [accounts[1], owner, amount]


def test_transfer_fails_on_imbalance(accounts, token, owner):
    token.mint(accounts[1], 100, {"from": owner})
    amount = token.balanceOf(accounts[1]) * 2
    with brownie.reverts("Insufficient balance"):
        token.transfer(owner, amount, {"from": accounts[1]})


def test_can_transfer_from_owner(accounts, token, owner):
    receiver_balance = token.balanceOf(owner)

    token.mint(accounts[1], 100, {"from": owner})
    amount = token.balanceOf(accounts[1]) // 4

    token.approve(owner, amount, {"from": accounts[1]})
    token.transferFrom(accounts[1], owner, amount, {"from": owner})

    assert token.balanceOf(owner) == receiver_balance + amount


def test_owner_can_transfer_owner(accounts, token, owner):
    new_owner = accounts[1]
    token.transfer_owner(new_owner, {"from": owner})
    init_bal = token.balanceOf(accounts[2])
    token.mint(accounts[2], 100, {"from": new_owner})
    assert token.balanceOf(accounts[2]) == 100 + init_bal


def test_nonowner_cannot_transfer_owner(accounts, token):
    new_owner = accounts[1]
    with brownie.reverts("Only owner"):
        token.transfer_owner(new_owner, {"from": accounts[2]})


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
