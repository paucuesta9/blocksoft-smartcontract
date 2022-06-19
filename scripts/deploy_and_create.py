from scripts.helpful_scripts import (
    get_account,
)
from brownie import Codes


def main():
    deploy_and_create()


def deploy_and_create():
    account = get_account()
    codes = Codes.deploy(
        {"from": account},
    )
    print(f"Codes contract address: {codes.address}")
    return codes
