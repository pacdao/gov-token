#!/usr/bin/python3
import brownie
import pytest
from brownie import ZERO_ADDRESS

def test_owner_can_mint(accounts, token):
    init_bal = token.balanceOf(accounts[1])
    token.mint(accounts[1], 100, {'from': accounts[0]})
    assert token.balanceOf(accounts[1]) == init_bal + 100

def test_nonowner_cannot_mint(accounts, token):
    with brownie.reverts("Only owner"):
        token.mint(accounts[1], 100, {'from': accounts[1]})

def test_can_transfer_to_owner(accounts, token):
    token.mint(accounts[1], 100, {'from': accounts[0]})

    init_balance = token.balanceOf(accounts[0])
    sender_balance = token.balanceOf(accounts[1])
    amount = sender_balance // 4
    assert amount > 0

    token.transfer(accounts[0], amount, {'from': accounts[1]})
    assert token.balanceOf(accounts[0]) == init_balance + amount

def test_transfer_event_fires(accounts, token):
    token.mint(accounts[1], 100, {'from': accounts[0]})
    amount = token.balanceOf(accounts[1])
    tx = token.transfer(accounts[0], amount, {'from': accounts[1]})

    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [accounts[1], accounts[0], amount]

def test_transfer_fails_on_imbalance(accounts, token):
    token.mint(accounts[1], 100, {'from': accounts[0]})
    amount = token.balanceOf(accounts[1]) * 2
    with brownie.reverts("Insufficient balance"):
        tx = token.transfer(accounts[0], amount, {'from': accounts[1]})



def test_cannot_transfer_to_nonowner(accounts, token):
    token.mint(accounts[1], 100, {'from': accounts[0]})
    recipient = accounts[2]
    init_bal = token.balanceOf(recipient)
    tx = token.transfer(recipient, token.balanceOf(accounts[1]), {'from': accounts[1]})
    assert tx.return_value == False
    assert token.balanceOf(recipient) == init_bal

def test_can_transfer_from_owner(accounts, token):
    receiver_balance = token.balanceOf(accounts[0])

    token.mint(accounts[1], 100, {'from': accounts[0]})
    amount = token.balanceOf(accounts[1]) // 4

    token.approve(accounts[0], amount, {'from': accounts[1]})
    token.transferFrom(accounts[1], accounts[0], amount, {'from': accounts[0]})

    assert token.balanceOf(accounts[0]) == receiver_balance + amount

def test_owner_can_transfer_owner(accounts, token):
    new_owner = accounts[1]
    token.transfer_owner(new_owner, {"from": accounts[0]})
    init_bal = token.balanceOf(accounts[2])
    token.mint(accounts[2], 100, {'from': new_owner})
    assert token.balanceOf(accounts[2]) == 100 + init_bal

def test_nonowner_cannot_transfer_owner(accounts, token):
    new_owner = accounts[1]
    with brownie.reverts("Only owner"):
        token.transfer_owner(new_owner, {"from": accounts[2]})
   
def test_mint_many_mints_many(accounts, token):
    list1 = []
    list2 = []
    for i in range(8):
        list1.append(accounts[i+1])
        list2.append(100)
    token.mintMany(list1, list2)
    for i in range(8):
        assert token.balanceOf(accounts[i+1]) == 100
def test_partial_mint_many_mints_many(accounts, token):
    list1 = []
    list2 = []
    for i in range(6):
        list1.append(accounts[i+1])
        list2.append(100)
    list1.append(ZERO_ADDRESS)
    list1.append(ZERO_ADDRESS)
    list2.append(0)
    list2.append(0)
    token.mintMany(list1, list2)
    for i in range(6):
        assert token.balanceOf(accounts[i+1]) == 100


