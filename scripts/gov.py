#!/usr/bin/python3

import brownie.network as network
from brownie import PacDaoGovernance, accounts
from brownie.network import max_fee, priority_fee


def main():

    if network.show_active() in ["mainnet", "mainnet-fork", "rinkeby"]:
        if network.show_active() == "mainnet":
            priority_fee("2 gwei")
            max_fee("55 gwei")
            publish = True
            account_name = "minnow"
        else:
            if network.show_active() != "mainnet-fork":
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

    return PacDaoGovernance.deploy(
        {"from": deployer},
        publish_source=publish,
    )
