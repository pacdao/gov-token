# @version 0.3.3

"""
@title Bare-bones Token implementation
@notice Based on the ERC-20 token standard as defined at
        https://eips.ethereum.org/EIPS/eip-20
"""


from vyper.interfaces import ERC20
implements: ERC20


event Approval:
    owner: indexed(address)
    spender: indexed(address)
    value: uint256

event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256

name: public(String[64]) 
symbol: public(String[32])
decimals: public(uint256)
totalSupply: public(uint256)

owner: public(address) 

balances: HashMap[address, uint256]
allowances: HashMap[address, HashMap[address, uint256]]

minters: public(DynArray[address, 16])

@external
def __init__():
        self.name = "PACDAO GOV"
        self.symbol = "PAC-G"
        self.decimals = 18
        self.totalSupply = 0
        self.owner = 0xf27AC88ac7e80487f21e5c2C847290b2AE5d7B8e 

@view
@external
def balanceOf(_owner: address) -> uint256:
    """
    @notice Getter to check the current balance of an address
    @param _owner Address to query the balance of
    @return Token balance
    """
    return self.balances[_owner]


@view
@external
def allowance(_owner : address, _spender : address) -> uint256:
    """
    @notice Getter to check the amount of tokens that an owner allowed to a spender
    @param _owner The address which owns the funds
    @param _spender The address which will spend the funds
    @return The amount of tokens still available for the spender
    """
    return self.allowances[_owner][_spender]


@external
def approve(_spender : address, _value : uint256) -> bool:
    """
    @notice Approve an address to spend the specified amount of tokens on behalf of msg.sender
    @dev Beware that changing an allowance with this method brings the risk that someone may use both the old
         and the new allowance by unfortunate transaction ordering. One possible solution to mitigate this
         race condition is to first reduce the spender's allowance to 0 and set the desired value afterwards:
         https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
    @param _spender The address which will spend the funds.
    @param _value The amount of tokens to be spent.
    @return Success boolean
    """
    self.allowances[msg.sender][_spender] = _value
    log Approval(msg.sender, _spender, _value)
    return True


@internal
def _transfer(_from: address, _to: address, _value: uint256):
    """
    @dev Internal shared logic for transfer and transferFrom
    """
    assert self.balances[_from] >= _value, "Insufficient balance"
    self.balances[_from] -= _value
    self.balances[_to] += _value
    log Transfer(_from, _to, _value)


@external
def transfer(_to : address, _value : uint256) -> bool:
    """
    @notice Transfer tokens to a specified address
    @dev Vyper does not allow underflows, so attempting to transfer more
         tokens than an account has will revert
    @param _to The address to transfer to
    @param _value The amount to be transferred
    @return Success boolean
    """
    self._transfer(msg.sender, _to, _value)
    return True



@external
def transferFrom(_from : address, _to : address, _value : uint256) -> bool:
    """
    @notice Transfer tokens from one address to another
    @dev Vyper does not allow underflows, so attempting to transfer more
         tokens than an account has will revert
    @param _from The address which you want to send tokens from
    @param _to The address which you want to transfer to
    @param _value The amount of tokens to be transferred
    @return Success boolean
    """
    assert self.allowances[_from][msg.sender] >= _value, "Insufficient allowance"
    self.allowances[_from][msg.sender] -= _value
    self._transfer(_from, _to, _value)
    return True

# Mint Functions

@internal
def _mint(_to : address, _amount : uint256):
    """
    @notice Internal Mint Function
    @dev Update mint
    @param _to The address to receive tokens
    @param _amount Amount of tokens to mint
    """
    self.balances[_to] += _amount
    self.totalSupply += _amount
    log Transfer(ZERO_ADDRESS, _to, _amount)


@external
def mint(to : address, amount : uint256):
    """
    @notice Mint Function
    @dev Mint function for accounts with minter role
    @param to The address to receive tokens
    @param amount Amount of tokens to mint
    """
    assert msg.sender == self.owner or msg.sender in self.minters, "Only minters"
    if to != ZERO_ADDRESS:
        self._mint(to, amount)


@external
def mint_many(to_list : address[8], value_list : uint256[8]):
    """
    @notice Mint in packs of Eight
    @dev Sender must have minter role, accepts batches of eight with ZERO_ADDRESS as empty
    @param to_list Up to eight addresses to receive tokens (ZERO_ADDR to skip)
    @param value_list Up to eight indexed values of tokens to mint
    """
    assert self.owner == msg.sender or msg.sender in self.minters, "Only owner"
    for i in range(8):
        if to_list[i] != ZERO_ADDRESS:
            self._mint(to_list[i], value_list[i])


@external
def transfer_owner(new_owner : address):
    """
    @notice Set contract owner 
    @dev Sender must be current owner 
    @param new_owner New contract owner address 
    """

    assert self.owner == msg.sender, "Only owner"
    self.owner = new_owner	

@external
def add_minter(new_addr : address):
    """
    @notice Add address as minter role
    @dev Sender must be current owner, fails on existing minter address
    @param new_addr New address to receive minting privilege
    """

    assert self.owner == msg.sender, "Only owner"
    assert new_addr not in self.minters, "Already exists"
    assert len(self.minters) < 16, "Too many minters"
    self.minters.append(new_addr)
	
@external
def revoke_minter(kill_addr: address):
    """
    @notice Remove address from minter role
    @dev Sender must be current owner, fails if address doesn't exist
    @param kill_addr New address to receive minting privilege
    """

    assert self.owner == msg.sender, "Only owner"
    assert kill_addr in self.minters, "Addr not found"
    new_minters : DynArray[address, 16] = []

    for i in range(16):
        if i < len(self.minters):
            if self.minters[i] != kill_addr and self.minters[i] != ZERO_ADDRESS:
                new_minters.append(self.minters[i])
    self.minters = new_minters


