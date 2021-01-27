from datetime import datetime, timedelta
from typing import List

from account_interface import AccountInterface


class CheckingAccount(AccountInterface):
    """
    This class implements a checking account without additional limit.
    This is a singleton class and the available limit and the card status
    are set at the instantiation by the constructor. The available limit is
    supposed to change only by calling transactions, also, all transactions are
    registered.
    """

    __instance = None
    __available_limit = 0
    __is_card_active = False
    __transactions = list()
    __violations = list()

    @staticmethod
    def get_instance():
        """
        Return an instance of the class if doesn't exists
        """
        if CheckingAccount.__instance is None:
            CheckingAccount()

        return CheckingAccount.__instance

    def __init__(self, available_limit: int, activate_card: bool) -> None:
        """
        Default constructor

        :param available_limit: Set the initial available limit
        :type available_limit: int

        :param activate_card: Set the inital card status
        :type activate_card: bool
        """
        # Make sure there will be only one instance
        if CheckingAccount.__instance is not None:
            raise Exception("Account id " + str(id(self)) + " already initialized")
        else:
            CheckingAccount.__instance = self

        # Set the initial limit, this generic account implementation doesn't
        # allows negative limits
        if type(available_limit) is int and available_limit > 0:
            self.__available_limit = available_limit
        else:
            raise ValueError("Account limit must be positive integer")

        # Set the card activation status
        if type(activate_card) is bool:
            self.__is_card_active = activate_card
        else:
            raise TypeError("Card activation status must be bool")

    def __repr__(self) -> str:
        """
        Return the formal string representation for the object

        :return: Formal representation
        :rtype: str
        """
        return "CheckingAccount(__available_limit='{}', __is_card_active='{}')".format(
            self.__available_limit, self.__is_card_active
        )

    def get_card_status(self) -> bool:
        """
        Return the activation card status

        :return: Card status
        :rtype: bool
        """
        return self.__is_card_active

    def get_transactions(self) -> List:
        """
        Return all the transactions performed for the account

        :return: Transactions performed
        :rtype: List
        """
        return self.__transactions

    def get_limit(self) -> int:
        """
        Return the available limit

        :return: Available limit
        :rtype: int
        """
        return self.__available_limit

    def get_violations(self) -> List:
        """
        Return all the reported violations for the account

        :return: Violations reported
        :rtype: List
        """
        return self.__violations

    def check_time_limit(self, final_time: str, initial_time: str, limit: int) -> bool:
        """
        Verify and return true if the time interval, delta, between final and
        initial timestamps is lesser or equal than the limit

        :param final_time: Final timestamp in the ISO format
        :type final_time: str

        :param initial_time: Initial timestamp in the ISO format
        :type initial_time: str

        :param limit: Time limit in minutes
        :type limit: int

        :return: True if the time interval is less or equal than the limit
        :rtype: bool
        """
        time_limit_in_minutes = timedelta(minutes=limit)
        t2 = datetime.fromisoformat(final_time.replace("Z", ""))
        t1 = datetime.fromisoformat(initial_time.replace("Z", ""))

        if (t2 - t1) <= time_limit_in_minutes:
            return True
        else:
            return False

    def validate_doubled_withdraw(
        self, merchant: str, amount: int, timestamp: str
    ) -> None:
        """
        Compare a given transaction to check and report if there is already
        another one for the same merchant and amount within the defined time
        window

        :param merchant: Merchant for the given transaction
        :type merchant: str

        :param amount: Amount for the given transaction
        :type: int

        :param timestamp: Timestamp in the ISO format for the given transaction
        :type: str
        """
        time_window_in_minutes = 2

        check = [
            self.check_time_limit(timestamp, t["time"], time_window_in_minutes)
            for t in self.__transactions
            if ((merchant == t["merchant"]) and (amount == t["amount"]))
        ]

        if True in check:
            self.__violations.append("doubled-transaction")

    def validate_withdraw_frequency(self, timestamp: str) -> None:
        """
        Compare the transaction based on its timestamp against the all the past
        transactions using a defined window of past transactions for a period
        of time and report if the current transaction exceeds this relation of
        transactions in the period of time

        :param timestamp: Timestamp in the ISO format for the given transaction
        :type: str
        """
        time_window_in_minutes = 2

        # Assure that at least two transactions already occured
        threshold = 2

        check = [
            self.check_time_limit(
                timestamp,
                self.__transactions[-threshold]["time"],
                time_window_in_minutes,
            )
            for t in self.__transactions
            if t["time"] and len(self.__transactions) > threshold
        ]

        if True in check:
            self.__violations.append("high-frequency-small-interval")

    def validate_withdraw_limit(self, amount: int) -> None:
        """
        Verify and report if the account has sufficient funds to the withdraw

        :param amount: Amount for the given transaction
        :type: int
        """
        if (self.__available_limit - amount) < 0:
            self.__violations.append("insufficient-limit")

    def withdraw_transaction(self, merchant: str, amount: int, timestamp: str) -> str:
        """
        Process and register a withdraw transaction based on the business rules

        :param merchant: Merchant for the given transaction
        :type merchant: str

        :param amount: Amount for the given transaction
        :type: int

        :param timestamp: Timestamp in the ISO format for the given transaction
        :type: str

        :return: A error message if occurs
        :rtype: str
        """
        # Clean-up the list of violations
        self.__violations = list()

        # Basic parameters verification
        if (
            type(merchant) is not str
            or type(amount) is not int
            or type(timestamp) is not str
            or amount <= 0
        ):
            self.__violations.append("wrong-or-missing-parameters")
            return self.__violations

        # Verify the withdraw against the business rules
        self.validate_withdraw_limit(amount)
        self.validate_doubled_withdraw(merchant, amount, timestamp)
        self.validate_withdraw_frequency(timestamp)

        # Process and register the transaction if no violations
        if len(self.__violations) == 0:
            self.__available_limit -= amount
            t = {"merchant": merchant, "amount": amount, "time": timestamp}
            self.__transactions.append(t)

        return self.__violations
