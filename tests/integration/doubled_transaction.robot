*** Settings ***
Library     Process
Library     OperatingSystem
Suite Teardown    Terminate All Processes    kill=True

Documentation
...
...     Output a violation when trying to authorize more than 1 transaction for the same merchand and amount in a time window of 2 minutes
...

*** Variables ***
${expected_output}      {"account": {"active_card": true, "available-limit": 90}, "violations": ["doubled-transaction"]}

*** Test Cases ***
Check Output
    ${result}           Run Process     /app/authorizer.py < /tests/integration/doubled_transaction.operations  shell=true
    Log                 ${result.stdout}
    Log                 ${result.stderr}
    Should Contain      ${result.stdout}    ${expected_output}
