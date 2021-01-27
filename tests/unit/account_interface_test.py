import pytest

from account_interface import AccountInterface


@pytest.fixture()
def account() -> AccountInterface:
    """
    Create an instance to be used across the test suite
    """
    # Set up
    account = AccountInterface()

    yield account


def test_get_limit_not_implemented(account: AccountInterface) -> None:
    """
    Test if calling the abstract method will fail
    """
    expected_output = "method not implemented"

    with pytest.raises(Exception) as e:
        assert account.get_limit()

    assert expected_output in str(e)


def test_get_transactions_not_implemented(account: AccountInterface) -> None:
    """
    Test if calling the abstract method will fail
    """
    expected_output = "method not implemented"

    with pytest.raises(Exception) as e:
        assert account.get_transactions()

    assert expected_output in str(e)
