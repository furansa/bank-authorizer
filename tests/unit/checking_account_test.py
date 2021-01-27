import datetime
import pytest

from checking_account import CheckingAccount


# Create an account instance to be used across the test suite
available_limit = 100
activate_card = True
account = CheckingAccount(available_limit, activate_card)
transactions = list()
violations = list()


# @pytest.mark.skip(reason="WiP")
def test_create_account_with_positive_limit_and_with_card_succeeds() -> None:
    """
    Test if the newly created account with positive limit and with active card
    succeeds
    """
    expected_available_limit = 100
    expected_activate_card = True

    assert (
        account.get_card_status() == expected_activate_card
        and account.get_limit() == expected_available_limit
    )


def test_repr_succeeds() -> None:
    """
    Test if the output of the official representation will succeed
    """
    expected_output = "CheckingAccount(__available_limit='{}', __is_card_active='{}')".format(
        available_limit, activate_card
    )

    assert repr(account) == expected_output


def test_recreate_account_fails() -> None:
    """
    Test if create recreate an account will fail
    """
    # Set up
    new_available_limit = 200
    new_activate_card = True

    with pytest.raises(Exception):
        CheckingAccount(new_available_limit, new_activate_card)


def test_validate_withdraw_limit_below_available_succees() -> None:
    """
    Test if validate a withdraw with with a positive value below the available
    limit will succeed
    """
    amount = 90
    expected_output = list()

    account.validate_withdraw_limit(amount)
    assert account.get_violations() == expected_output


def test_validate_withdraw_limit_above_available_fails() -> None:
    """
    Test if validate a withdraw with with a positive value above the available
    limit will fail
    """
    amount = 110
    expected_output = ["insufficient-limit"]

    account.validate_withdraw_limit(amount)
    assert account.get_violations() == expected_output


def test_withdraw_transaction_with_positive_value_below_limit_succeeds() -> None:
    """
    Test if a withdraw transaction with a positive value below the available
    limit will succeed
    """
    merchant = "Test merchant 1"
    amount = 10
    ts = "{}Z".format(datetime.datetime.utcnow().isoformat(timespec="milliseconds"))
    # Append to the transaction list in order to use on a later test
    transactions.append({"merchant": merchant, "amount": amount, "time": ts})

    expected_output = list()

    assert account.withdraw_transaction(merchant, amount, ts) == expected_output


def test_withdraw_transaction_with_positive_value_equal_limit_succeeds() -> None:
    """
    Test if a withdraw transaction with a positive value equal the available
    limit will succeed
    """
    merchant = "Test merchant 2"
    amount = 20
    ts = "{}Z".format(datetime.datetime.utcnow().isoformat(timespec="milliseconds"))
    # Append to the transaction list which will be checked later
    transactions.append({"merchant": merchant, "amount": amount, "time": ts})

    expected_output = list()

    assert account.withdraw_transaction(merchant, amount, ts) == expected_output


def test_withdraw_positive_value_above_limit_fails() -> None:
    """
    Test if withdraw a positive value above the available limit will fail
    """
    merchant = "Test merchant 3"
    amount = 100
    ts = "{}Z".format(datetime.datetime.utcnow().isoformat(timespec="milliseconds"))

    expected_output = ["insufficient-limit"]

    assert account.withdraw_transaction(merchant, amount, ts) == expected_output


def test_withdraw_zero_value_fails() -> None:
    """
    Test if withdraw a zero value will fail
    """
    merchant = "Test merchant 4"
    amount = 0
    ts = "{}Z".format(datetime.datetime.utcnow().isoformat(timespec="milliseconds"))

    expected_output = ["wrong-or-missing-parameters"]

    assert account.withdraw_transaction(merchant, amount, ts) == expected_output


def test_withdraw_negative_value_fails() -> None:
    """
    Test if withdraw a negative value will fail
    """
    merchant = "Test merchant 5"
    amount = -10
    ts = "{}Z".format(datetime.datetime.utcnow().isoformat(timespec="milliseconds"))

    expected_output = ["wrong-or-missing-parameters"]
    # Append to the violation list in order to use on a later test
    violations.append(expected_output[0])

    assert account.withdraw_transaction(merchant, amount, ts) == expected_output


def test_get_transactions_succeeds() -> None:
    """
    Test if return all the transactions already performed will succeed
    """
    expected_output = transactions

    assert account.get_transactions() == expected_output


def test_get_violations_succeeds() -> None:
    """
    Test if return registered violations for the last transaction will succeed
    """
    expected_output = violations

    assert account.get_violations() == expected_output


def test_check_time_limit_below_succeeds() -> None:
    """
    Test if return is correct for a given time delta which does not exceeds the
    time limit
    """
    initial_time = "2020-12-28T09:00:00.000Z"
    final_time = "2020-12-28T09:04:00.000Z"
    time_limit = 5
    expected_output = True

    assert (
        account.check_time_limit(final_time, initial_time, time_limit)
        == expected_output
    )


def test_check_time_limit_above_fails() -> None:
    """
    Test if return is correct for a given time delta which exceeds the time
    limit
    """
    initial_time = "2020-12-28T09:00:00.000Z"
    final_time = "2020-12-28T09:06:00.000Z"
    time_limit = 5
    expected_output = False

    assert (
        account.check_time_limit(final_time, initial_time, time_limit)
        == expected_output
    )


def test_validate_double_withdraw_succeeds() -> None:
    """
    Test if violation report for doubled withdraw will succeed
    """
    # Retrieve data from the latest successful transaction and repeat it
    merchant = transactions[-1]["merchant"]
    amount = transactions[-1]["amount"]
    time = transactions[-1]["time"]

    account.validate_doubled_withdraw(merchant, amount, time)

    # The violations list already contains an item from previous tests
    expected_output = ["wrong-or-missing-parameters", "doubled-transaction"]

    assert account.get_violations() == expected_output


def test_validate_withdraw_frequency_succeeds() -> None:
    """
    Test if violation report for high frequency small interval will succeed
    """
    # The violations list already contains an item from previous tests
    expected_output = ["high-frequency-small-interval"]

    # Register a third transaction since there are already two successfully
    # registered
    merchant = "Test merchant 3"
    amount = 30
    ts = "{}Z".format(datetime.datetime.utcnow().isoformat(timespec="milliseconds"))
    # Append to the transaction list which will be checked later
    transactions.append({"merchant": merchant, "amount": amount, "time": ts})

    account.withdraw_transaction(merchant, amount, ts)

    assert len(transactions) == 3

    # Simulate a forth transaction timestamp in a two-minute interval in order
    # to trigger the validation
    time = transactions[-1]["time"]

    account.validate_withdraw_frequency(time)

    assert account.get_violations() == expected_output
