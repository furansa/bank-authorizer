*** Settings ***
Library     Process
Library     OperatingSystem
Suite Teardown    Terminate All Processes    kill=True

Documentation
...
...     Output a violation when trying to authorize a transaction without an active card
...

*** Variables ***
${expected_output}      {"account": {"active_card": false, "available-limit": 100}, "violations": ["card-not-active"]}

*** Test Cases ***
Check Output
    ${result}           Run Process     /app/authorizer.py < /tests/integration/card_not_active.operations  shell=true
    Log                 ${result.stdout}
    Log                 ${result.stderr}
    Should Contain      ${result.stdout}    ${expected_output}
