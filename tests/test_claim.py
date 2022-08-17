import brownie


def test_only_owner_can_claim_erc20(token, accounts, dummy_token):
    dummy_token.mint(token, 10**18, {"from": dummy_token.owner()})
    with brownie.reverts("Only owner"):
        dummy_token.claim_erc20(dummy_token, {"from": accounts[1]})


def test_claim_erc20_from_token(token, accounts, dummy_token):
    dummy_token.mint(token, 10**18, {"from": dummy_token.owner()})
    assert dummy_token.balanceOf(token) == 10**18
    assert dummy_token.balanceOf(token.owner()) == 0

    token.claim_erc20(dummy_token, {"from": token.owner()})
    assert dummy_token.balanceOf(token) == 0
    assert dummy_token.balanceOf(token.owner()) == 10**18


def test_claim_erc20_from_bridge(minter, token, accounts, dummy_token):
    assert dummy_token.balanceOf(minter) == 0
    assert dummy_token.balanceOf(token) == 0

    dummy_token.mint(minter, 10**18, {"from": dummy_token.owner()})
    assert dummy_token.balanceOf(minter) == 10**18
    minter.withdraw_erc20(
        dummy_token, 10**18, {"from": "0xf27AC88ac7e80487f21e5c2C847290b2AE5d7B8e"}
    )

    assert dummy_token.balanceOf(minter) == 0
    assert dummy_token.balanceOf(token) == 10**18


def test_only_owner_can_claim_from_bridge(minter, token, accounts, dummy_token):
    dummy_token.mint(minter, 10**18, {"from": dummy_token.owner()})

    with brownie.reverts("Only owner"):
        minter.withdraw_erc20(dummy_token, 10**18, {"from": accounts[0]})
