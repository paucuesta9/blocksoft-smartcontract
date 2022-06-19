import pytest
from brownie import network, Codes, accounts
import brownie
from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS
)


def test_can_create_code():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    codes = Codes.deploy(
        {"from": get_account()},
    )
    # Act
    transaction_receipt = codes.createCode(
        "None", False, {"from": get_account()}
    )
    # Assert
    assert isinstance(transaction_receipt.txid, str)
    assert codes._tokenIds() > 0
    assert isinstance(codes._tokenIds(), int)

def test_can_transfer_code():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    codes = Codes.deploy(
        {"from": get_account()},
    )
    # Act
    transaction_receipt = codes.createCode(
        "None", False, {"from": get_account()}
    )
    tx = codes.transferCode(1, '0xcb5c1869Eb7F0d99C8225378d48E17135bF15975', {"from": get_account()})
    # Assert
    assert isinstance(tx.txid, str)

def test_transfer_to_yourself_fails():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    codes = Codes.deploy(
        {"from": get_account()},
    )
    # Act
    transaction_receipt = codes.createCode(
        "None", False, {"from": get_account()}
    )
    # Assert reverts
    with brownie.reverts():
        tx = codes.transferCode(1, get_account(), {"from": get_account()})

def test_transfer_not_owner_fails():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    codes = Codes.deploy(
        {"from": get_account()},
    )
    # Act
    transaction_receipt = codes.createCode(
        "None", False, {"from": accounts[1]}
    )
    # Assert reverts
    with brownie.reverts():
        tx = codes.transferCode(1, get_account(), {"from": get_account()})

def test_fetch_codes():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    codes = Codes.deploy(
        {"from": get_account()},
    )
    # Act
    transaction_receipt = codes.createCode(
        "None", False, {"from": get_account()}
    )
    tx = codes.fetchCodes({"from": get_account()})
    # Assert
    assert isinstance(tx, brownie.convert.datatypes.ReturnValue)

def test_fetch_user_owner_codes():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    codes = Codes.deploy(
        {"from": get_account()},
    )
    # Act
    transaction_receipt = codes.createCode(
        "None", False, {"from": get_account()}
    )
    tx = codes.fetchUserOwnerCodes(get_account(), {"from": get_account()})

    # Assert
    assert isinstance(tx, brownie.convert.datatypes.ReturnValue)

def test_fetch_codes_created_by_user():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    codes = Codes.deploy(
        {"from": get_account()},
    )
    # Act
    transaction_receipt = codes.createCode(
        "None", False, {"from": get_account()}
    )
    tx = codes.fetchCodesCreatedByUser(get_account(), {"from": get_account()})

    # Assert
    assert isinstance(tx, brownie.convert.datatypes.ReturnValue)

def test_fetch_codes_by_token():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    codes = Codes.deploy(
        {"from": get_account()},
    )
    # Act
    transaction_receipt = codes.createCode(
        "None", False, {"from": get_account()}
    )
    tx = codes.fetchCodesByToken([1], {"from": get_account()})

    # Assert
    assert isinstance(tx, brownie.convert.datatypes.ReturnValue)

def test_fetch_code():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    codes = Codes.deploy(
        {"from": get_account()},
    )
    # Act
    transaction_receipt = codes.createCode(
        "None", False, {"from": get_account()}
    )
    tx = codes.fetchCode(1, {"from": get_account()})

    # Assert
    assert isinstance(tx, brownie.convert.datatypes.ReturnValue)

def test_fetch_code_private_not_owner():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    codes = Codes.deploy(
        {"from": get_account()},
    )
    # Act
    transaction_receipt = codes.createCode(
        "None", True, {"from": get_account()}
    )
    # Assert reverts
    with brownie.reverts():
        tx = codes.fetchCode(1, {"from": accounts[1]})
