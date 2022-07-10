#!/usr/bin/python3

import brownie.network as network
from brownie import Contract, PacDaoGovernance, PacGovFungible, accounts, PacGovBridge
from brownie.network import max_fee, priority_fee


def main():

    if network.show_active() in ["mainnet", "mainnet-fork", "mainnet-fork-alchemy", "rinkeby"]:
        if network.show_active() == "mainnet":
            priority_fee("2 gwei")
            max_fee(input("Max fee (gwei): "))
            publish = True
            account_name = "minnow"
        else:
            if network.show_active() not in ['mainnet-fork', 'mainnet-fork-alchemy']:
                publish = True
            else:
                publish = False
            account_name = "husky"

        deployer = accounts.load(account_name)
        beneficiary_address = "0xf27AC88ac7e80487f21e5c2C847290b2AE5d7B8e"

    else:
        deployer = accounts[0]
        publish = False
        beneficiary_address = deployer

    gov2 = PacGovFungible.deploy(
        {"from": deployer},
        publish_source=publish,
    )
    gov = Contract('0x3459cfce9c0306eb1d5d0e2b78144c9fbd94c87b')
    gov.transferOwner(gov2, {'from': beneficiary_address})
    
    bridge = PacGovBridge.deploy(gov2, {'from': deployer} )
    gov2.add_minter(bridge, {"from": beneficiary_address})
    return gov2
