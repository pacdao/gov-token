#!/usr/bin/python3
import brownie


def test_owner_can_mint(accounts, token, owner):
    init_bal = token.balanceOf(accounts[1])
    token.mint(accounts[1], 100, {"from": owner})
    assert token.balanceOf(accounts[1]) == init_bal + 100


def test_nonminter_cannot_mint(accounts, token):
    with brownie.reverts("Only minters"):
        token.mint(accounts[1], 100, {"from": accounts[1]})


def test_owner_can_mint_many(token, accounts, owner):
    init_bal = token.balanceOf(accounts[1])
    token.mint_many([accounts[1]] * 8, [100] * 8, {"from": owner})
    assert token.balanceOf(accounts[1]) == init_bal + 800


def test_nonminter_cannot_mint_many(token, accounts):
    with brownie.reverts("Only minters"):
        token.mint_many([accounts[0]] * 8, [1000] * 8, {"from": accounts[1]})


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


def test_transfer_owner_fires_event(token, owner, accounts):
    tx = token.transfer_owner(accounts[1], {"from": owner})
    assert tx.events["NewOwner"] == [accounts[1]]
