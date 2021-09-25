#!/usr/bin/python3

from brownie import PacDaoGovernance, accounts


def main():
    return PacDaoGovernance.deploy("PACDAO GOV", "PDGOV", 18, 1e21, {'from': accounts[0]})
