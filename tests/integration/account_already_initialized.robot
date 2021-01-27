*** Settings ***
Library     Process
Library     OperatingSystem
Suite Teardown    Terminate All Processes    kill=True

Documentation
...
...     Output a violation when trying to recreate an account
...

*** Variables ***
${expected_output}      {"account": {"active_card": true, "available-limit": 100}, "violations": ["account-already-initialized"]}

*** Test Cases ***
Check Output
    ${result}           Run Process     /app/authorizer.py < /tests/integration/account_already_initialized.operations  shell=true
    Log                 ${result.stdout}
    Log                 ${result.stderr}
    Should Contain      ${result.stdout}    ${expected_output}
