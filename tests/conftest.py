#!/usr/bin/python3

import pytest
from brownie import Contract


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def token(PacGovFungible, accounts):
    v2_token = PacGovFungible.deploy({"from": accounts[0]})
    v1_token = Contract(v2_token.v1_token())
    multisig = v1_token.owner()
    v1_token.transferOwner(v2_token, {"from": v1_token.owner()})
    v2_token.transferOwner(multisig, {"from": v2_token.owner()})
    v2_token.mint(accounts[0], 1000 * 10 ** v2_token.decimals(), {"from": multisig})
    return v2_token


@pytest.fixture(scope="module")
def owner(token):
    return token.owner()


@pytest.fixture(scope="module")
def v1_token(token):
    return Contract(token.v1_token())


@pytest.fixture(scope="module")
def v1_hodler(token, v1_token):
    hodler = "0x6215181b1f33af4f0b60125017e72d3615dcd6e3"
    v1_token.approve(token, v1_token.balanceOf(hodler), {"from": hodler})
    return hodler
