*** Settings ***
Library     Process
Library     OperatingSystem
Suite Teardown    Terminate All Processes    kill=True

Documentation
...
...     Output a violation when trying to authorize more than 3 transactions in a time window of 2 minutes
...

*** Variables ***
${expected_output}      {"account": {"active_card": true, "available-limit": 40}, "violations": ["high-frequency-small-interval"]}

*** Test Cases ***
Check Output
    ${result}           Run Process     /app/authorizer.py < /tests/integration/high_frequency_small_interval.operations  shell=true
    Log                 ${result.stdout}
    Log                 ${result.stderr}
    Should Contain      ${result.stdout}    ${expected_output}
