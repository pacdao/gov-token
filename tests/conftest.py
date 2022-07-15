#!/usr/bin/python3

import pytest
from brownie import Contract


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def token(PacGovFungible, accounts, v1_token):
    v2_token = PacGovFungible.deploy({"from": accounts[0]})
    multisig = v1_token.owner()
    v2_token.transfer_owner(multisig, {"from": v2_token.owner()})
    v2_token.mint(accounts[0], 1000 * 10 ** v2_token.decimals(), {"from": multisig})
    return v2_token


@pytest.fixture(scope="module")
def owner(token):
    return token.owner()


@pytest.fixture(scope="module")
def minter(token, PacGovBridge, owner, v1_token):
    bridge = PacGovBridge.deploy(token, {"from": owner})
    token.update_minter(bridge, {"from": owner})
    v1_token.transferOwner(bridge, {"from": v1_token.owner()})

    return bridge


@pytest.fixture(scope="module")
def v1_token():
    return Contract("0x3459cfCe9c0306EB1D5D0e2b78144C9FBD94c87B")


@pytest.fixture(scope="module")
def v1_hodler_addr():
    return "0x6215181b1f33af4f0b60125017e72d3615dcd6e3"


@pytest.fixture(scope="module")
def v1_hodler(v1_token, minter, v1_hodler_addr):
    v1_token.approve(
        minter, v1_token.balanceOf(v1_hodler_addr), {"from": v1_hodler_addr}
    )
    return v1_hodler_addr

@pytest.fixture(scope="module")
def v2_hodler(token, v1_hodler, minter):
    minter.upgrade(v1_hodler, {'from': v1_hodler})
    assert token.balanceOf(v1_hodler) > 0
    return v1_hodler
