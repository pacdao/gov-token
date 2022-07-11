# @version 0.3.3

"""
@title PAC DAO v2 Gov Token Bridge
@notice Based on the ERC-20 token standard as defined at
        https://eips.ethereum.org/EIPS/eip-20
"""

from vyper.interfaces import ERC20

interface MintableToken:
    def mint(to :address, amount: uint256): nonpayable


v1_token: public(ERC20)
gov_token: public(MintableToken)

@external
def __init__(gov_token : address):
    self.v1_token = ERC20(0x3459cfCe9c0306EB1D5D0e2b78144C9FBD94c87B)
    self.gov_token = ERC20(gov_token)

@external
def upgrade(to_addr : address):
    assert self.v1_token.balanceOf(to_addr) > 0, "No balance"
    _balance: uint256 = self.v1_token.balanceOf(to_addr)
    assert self.v1_token.allowance(to_addr, self) >= _balance, "No Approval"

    self.v1_token.transferFrom(to_addr, self, self.v1_token.balanceOf(to_addr))
    self.gov_token.mint(to_addr, _balance)


