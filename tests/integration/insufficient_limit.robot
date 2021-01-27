*** Settings ***
Library     Process
Library     OperatingSystem
Suite Teardown    Terminate All Processes    kill=True

Documentation
...
...     Output a violation when trying to authorize a transaction without available limit
...

*** Variables ***
${expected_output}      {"account": {"active_card": true, "available-limit": 50}, "violations": ["insufficient-limit"]}

*** Test Cases ***
Check Output
    ${result}           Run Process     /app/authorizer.py < /tests/integration/insufficient_limit.operations  shell=true
    Log                 ${result.stdout}
    Log                 ${result.stderr}
    Should Contain      ${result.stdout}    ${expected_output}
