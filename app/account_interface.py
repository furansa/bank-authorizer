from typing import List


class AccountInterface:
    """
    This informal interface is a reference for an account and all classes must
    implement its own versions for each specific case
    """

    def get_limit(self) -> int:
        """
        Return the available limit

        :return: Available limit
        :rtype: int
        """
        raise NotImplementedError("method not implemented")

    def get_transactions(self) -> List:
        """
        Return all the transactions performed for the account

        :return: Transactions performed
        :rtype: List
        """
        raise NotImplementedError("method not implemented")
