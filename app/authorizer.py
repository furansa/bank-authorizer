#!/usr/bin/env python3
#
# @file      authorizer.sh
# @author    Me :-)
# @version   0.0.1
# @brief     Main application
#
import fileinput  # pragma: no cover
import json  # pragma: no cover
import os  # pragma: no cover

from checking_account import CheckingAccount  # pragma: no cover

# Debug mode outputs to stdout detailed information about each line processed
DEBUG_MODE = os.environ["APP_DEBUG_MODE"]  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    """
    Main program entrypoint
    """
    if DEBUG_MODE == "True":
        print("DEBUG: Debug mode enabled")

    # Initial account status
    account = None
    active_card = False
    available_limit = 0

    # Initial transaction status
    merchant = ""
    amount = 0
    time = ""
    violations = list()

    # Process the request from the input stream
    current_line = 0

    for line in fileinput.input():
        current_line += 1

        if DEBUG_MODE == "True":
            print("\nDEBUG: Reading line {}: {}".format(current_line, line))

        # Decode request data into json
        json_data = json.loads(line)

        # Identify the type operation type and process accordingly
        operation_type = list(json_data.keys())[0]

        if operation_type == "account":
            if account is None:
                # Create a new account
                active_card = json_data[operation_type]["active-card"]
                available_limit = json_data[operation_type]["available-limit"]
                account = CheckingAccount(available_limit, active_card)
            else:
                violations.append("account-already-initialized")

        if operation_type == "transaction":
            if account is None:
                violations.append("account-not-initialized")
            elif active_card is False:
                violations.append("card-not-active")
            else:
                # Retrieve data from the operation to process the transaction
                merchant = json_data[operation_type]["merchant"]
                amount = json_data[operation_type]["amount"]
                time = json_data[operation_type]["time"]

        # Perform the transaction and report the response along with any
        # operation violation
        if operation_type == "transaction" and len(violations) == 0:
            response = account.withdraw_transaction(merchant, amount, time)

            if len(response) > 0:
                [violations.append(r) for r in response]

            # Update the limit after the transaction
            available_limit = account.get_limit()

        # Output the response and clean-up the list of violations
        output_data = {
            "account": {"active_card": active_card, "available-limit": available_limit},
            "violations": violations,
        }

        output_json = json.dumps(output_data)

        print(output_json)

        violations = list()
