# Authorizer

Authorizer is an application which receive, process and authorize bank account
operations by using a pre-defined set of rules.

The events comes from the STDIN in a form of a stream of data to be processed
one by one and then returned to the STDOUT.

## Building and Running

The application use Python and run inside a Docker container which make it easy
to build, deploy and scale across many environments. The following images are
provided:

* Development, which run the application with a more verbose output in order to
help on debugging
* Test, which doesn't run the application but the unit and system (integration)
tests and generate both test and coverage reports
* Production, which run the application in the normal operation mode

To build and run the application in foreground choose from the described images
and run ```docker-compose -f docker-compose-{environment}.yaml up``` in a terminal
from the same directory where the ```docker-compose-{environment}.yaml``` file
is and ```environment``` can be ```dev```, ```test``` or ```prod```.

The file containing the operations to be processed must be saved under the
```app/operations``` file. The cointainer will build its image, run and process
the operations file outputing the result for each processed operations and goes
down after finish, for example:

```shell
$ docker-compose -f docker-compose-prod.yaml up
Building authorizer
Step 1/9 : FROM python:3.8-slim
...
Step 9/9 : ENTRYPOINT ["/tmp/entrypoint.sh"]
...
Successfully tagged autorizer:prod
...
Recreating authorizer ... done
Attaching to authorizer
authorizer    | {"account": {"active_card": false, "available-limit": 0}, "violations": ["account-not-initialized"]}
authorizer    | {"account": {"active_card": false, "available-limit": 0}, "violations": ["account-not-initialized"]}
authorizer    | {"account": {"active_card": true, "available-limit": 80}, "violations": []}
authorizer    | {"account": {"active_card": true, "available-limit": 75}, "violations": []}
authorizer    | {"account": {"active_card": true, "available-limit": 65}, "violations": []}
authorizer    | {"account": {"active_card": true, "available-limit": 65}, "violations": ["high-frequency-small-interval"]}
authorizer    | {"account": {"active_card": true, "available-limit": 65}, "violations": ["account-already-initialized"]}
authorizer    | {"account": {"active_card": true, "available-limit": 60}, "violations": []}
authorizer    | {"account": {"active_card": true, "available-limit": 60}, "violations": ["doubled-transaction"]}
authorizer    | {"account": {"active_card": true, "available-limit": 56}, "violations": []}
authorizer    | {"account": {"active_card": true, "available-limit": 46}, "violations": []}
authorizer    | {"account": {"active_card": true, "available-limit": 46}, "violations": ["insufficient-limit"]}
authorizer    | {"account": {"active_card": true, "available-limit": 46}, "violations": ["insufficient-limit"]}
authorizer    | {"account": {"active_card": true, "available-limit": 46}, "violations": ["account-already-initialized"]}
authorizer exited with code 0
```

The ```docker-compose-dev.yaml``` run the application in debug mode, which will
show the detail about the line being processed, for example:

```shell
$ docker-compose -f docker-compose-dev.yaml up
Building authorizer
Step 1/9 : FROM python:3.8-slim
...
Step 9/9 : ENTRYPOINT ["/tmp/entrypoint.sh"]
...
Successfully tagged autorizer:dev
...
Recreating authorizer ... done
Attaching to authorizer
authorizer    | DEBUG: Debug mode enabled
authorizer    | 
authorizer    | DEBUG: Reading line 1: {"transaction": {"merchant": "Habbib's", "amount": 10, "time": "2019-02-13T10:00:00.000Z"}}
authorizer    | 
authorizer    | {"account": {"active_card": false, "available-limit": 0}, "violations": ["account-not-initialized"]}
authorizer    | 
authorizer    | DEBUG: Reading line 2: {"transaction": {"merchant": "Habbib's", "amount": 10, "time": "2019-02-13T10:01:00.000Z"}}
authorizer    | 
authorizer    | {"account": {"active_card": false, "available-limit": 0}, "violations": ["account-not-initialized"]}
authorizer    | 
authorizer    | DEBUG: Reading line 3: {"account": {"active-card": true, "available-limit": 80}}
authorizer    | 
authorizer    | {"account": {"active_card": true, "available-limit": 80}, "violations": []}
authorizer    | 
authorizer    | DEBUG: Reading line 4: {"transaction": {"merchant": "Habbib's", "amount": 5, "time": "2019-02-13T10:02:00.000Z"}}
authorizer    | 
authorizer    | {"account": {"active_card": true, "available-limit": 75}, "violations": []}
authorizer    | 
authorizer    | DEBUG: Reading line 5: {"transaction": {"merchant": "Burger King", "amount": 10, "time": "2019-02-13T10:03:00.000Z"}}
authorizer    | 
authorizer    | {"account": {"active_card": true, "available-limit": 65}, "violations": []}
authorizer    | 
authorizer    | DEBUG: Reading line 6: {"transaction": {"merchant": "McDonald's", "amount": 15, "time": "2019-02-13T10:04:00.000Z"}}
authorizer    | 
authorizer    | {"account": {"active_card": true, "available-limit": 65}, "violations": ["high-frequency-small-interval"]}
authorizer    | 
authorizer    | DEBUG: Reading line 7: {"account": {"active-card": true, "available-limit": 80}}
authorizer    | 
authorizer    | {"account": {"active_card": true, "available-limit": 65}, "violations": ["account-already-initialized"]}
authorizer    | 
authorizer    | DEBUG: Reading line 8: {"transaction": {"merchant": "Habbib's", "amount": 5, "time": "2019-02-13T10:05:00.111Z"}}
authorizer    | 
authorizer    | {"account": {"active_card": true, "available-limit": 60}, "violations": []}
authorizer    | 
authorizer    | DEBUG: Reading line 9: {"transaction": {"merchant": "Habbib's", "amount": 5, "time": "2019-02-13T10:07:00.111Z"}}
authorizer    | 
authorizer    | {"account": {"active_card": true, "available-limit": 60}, "violations": ["doubled-transaction"]}
authorizer    | 
authorizer    | DEBUG: Reading line 10: {"transaction": {"merchant": "McDonald's", "amount": 4, "time": "2019-02-13T10:08:00.333Z"}}
authorizer    | 
authorizer    | {"account": {"active_card": true, "available-limit": 56}, "violations": []}
authorizer    | 
authorizer    | DEBUG: Reading line 11: {"transaction": {"merchant": "Burger King", "amount": 10, "time": "2019-02-13T10:09:00.444Z"}}
authorizer    | 
authorizer    | {"account": {"active_card": true, "available-limit": 46}, "violations": []}
authorizer    | 
authorizer    | DEBUG: Reading line 12: {"transaction": {"merchant": "Habbib's", "amount": 50, "time": "2019-02-13T10:30:00.000Z"}}
authorizer    | 
authorizer    | {"account": {"active_card": true, "available-limit": 46}, "violations": ["insufficient-limit"]}
authorizer    | 
authorizer    | DEBUG: Reading line 13: {"transaction": {"merchant": "Habbib's", "amount": 50, "time": "2019-02-13T10:31:00.000Z"}}
authorizer    | 
authorizer    | {"account": {"active_card": true, "available-limit": 46}, "violations": ["insufficient-limit"]}
authorizer    | 
authorizer    | DEBUG: Reading line 14: {"account": {"active-card": true, "available-limit": 80}}
authorizer    | 
authorizer    | {"account": {"active_card": true, "available-limit": 46}, "violations": ["account-already-initialized"]}
authorizer exited with code 0
```

## Testing

The ```docker-compose-test.yaml``` run the unit and system (integration) tests
using the PyTest and Robot frameworks, generating the reports after that,
for example:

```shell
$ docker-compose -f docker-compose-test.yaml up
Building authorizer
Step 1/9 : FROM python:3.8-slim
...
Step 9/9 : ENTRYPOINT ["/tmp/entrypoint.sh"]
...
Successfully tagged autorizer:test
...
Creating authorizer ... done
Attaching to authorizer
authorizer    | Starting the unit tests
authorizer    | ============================= test session starts ==============================
authorizer    | platform linux -- Python 3.8.6, pytest-6.2.1, py-1.10.0, pluggy-0.13.1 -- /usr/local/bin/python
authorizer    | cachedir: .pytest_cache
authorizer    | metadata: {'Python': '3.8.6', 'Platform': 'Linux-5.4.0-59-generic-x86_64-with-glibc2.2.5', 'Packages': {'pytest': '6.2.1', 'py': '1.10.0', 'pluggy': '0.13.1'}, 'Plugins': {'cov': '2.10.1', 'metadata': '1.11.0', 'html': '3.1.1'}}
authorizer    | rootdir: /tests/unit
authorizer    | plugins: cov-2.10.1, metadata-1.11.0, html-3.1.1
authorizer    | collecting ... collected 18 items
authorizer    |
authorizer    | ../tests/unit/account_interface_test.py::test_get_limit_not_implemented PASSED [  5%]
authorizer    | ../tests/unit/account_interface_test.py::test_get_transactions_not_implemented PASSED [ 11%]
authorizer    | ../tests/unit/checking_account_test.py::test_create_account_with_positive_limit_and_with_card_succeeds PASSED [ 16%]
authorizer    | ../tests/unit/checking_account_test.py::test_repr_succeeds PASSED        [ 22%]
authorizer    | ../tests/unit/checking_account_test.py::test_recreate_account_fails PASSED [ 27%]
authorizer    | ../tests/unit/checking_account_test.py::test_validate_withdraw_limit_below_available_succees PASSED [ 33%]
authorizer    | ../tests/unit/checking_account_test.py::test_validate_withdraw_limit_above_available_fails PASSED [ 38%]
authorizer    | ../tests/unit/checking_account_test.py::test_withdraw_transaction_with_positive_value_below_limit_succeeds PASSED [ 44%]
authorizer    | ../tests/unit/checking_account_test.py::test_withdraw_transaction_with_positive_value_equal_limit_succeeds PASSED [ 50%]
authorizer    | ../tests/unit/checking_account_test.py::test_withdraw_positive_value_above_limit_fails PASSED [ 55%]
authorizer    | ../tests/unit/checking_account_test.py::test_withdraw_zero_value_fails PASSED [ 61%]
authorizer    | ../tests/unit/checking_account_test.py::test_withdraw_negative_value_fails PASSED [ 66%]
authorizer    | ../tests/unit/checking_account_test.py::test_get_transactions_succeeds PASSED [ 72%]
authorizer    | ../tests/unit/checking_account_test.py::test_get_violations_succeeds PASSED [ 77%]
authorizer    | ../tests/unit/checking_account_test.py::test_check_time_limit_below_succeeds PASSED [ 83%]
authorizer    | ../tests/unit/checking_account_test.py::test_check_time_limit_above_fails PASSED [ 88%]
authorizer    | ../tests/unit/checking_account_test.py::test_validate_double_withdraw_succeeds PASSED [ 94%]
authorizer    | ../tests/unit/checking_account_test.py::test_validate_withdraw_frequency_succeeds PASSED [100%]
authorizer    |
authorizer    | ---- generated html file: file:///tests/reports/unit/2021-01-05_022147.html ----
authorizer    |
authorizer    | ----------- coverage: platform linux, python 3.8.6-final-0 -----------
authorizer    | Coverage HTML written to dir /tests/reports/unit/coverage
authorizer    |
authorizer    | ============================== 18 passed in 0.14s ==============================
authorizer    | Starting the integration tests
authorizer    | ==============================================================================
authorizer    | Integration
authorizer    | ==============================================================================
authorizer    | Integration.Account Already Initialized
authorizer    | ==============================================================================
authorizer    | Check Output                                                          | PASS |
authorizer    | ------------------------------------------------------------------------------
authorizer    | Integration.Account Already Initialized                               | PASS |
authorizer    | 1 critical test, 1 passed, 0 failed
authorizer    | 1 test total, 1 passed, 0 failed
authorizer    | ==============================================================================
authorizer    | Integration.Account Not Initialized
authorizer    | ==============================================================================
authorizer    | Check Output                                                          | PASS |
authorizer    | ------------------------------------------------------------------------------
authorizer    | Integration.Account Not Initialized                                   | PASS |
authorizer    | 1 critical test, 1 passed, 0 failed
authorizer    | 1 test total, 1 passed, 0 failed
authorizer    | ==============================================================================
authorizer    | Integration.Card Not Active
authorizer    | ==============================================================================
authorizer    | Check Output                                                          | PASS |
authorizer    | ------------------------------------------------------------------------------
authorizer    | Integration.Card Not Active                                           | PASS |
authorizer    | 1 critical test, 1 passed, 0 failed
authorizer    | 1 test total, 1 passed, 0 failed
authorizer    | ==============================================================================
authorizer    | Integration.Doubled Transaction
authorizer    | ==============================================================================
authorizer    | Check Output                                                          | PASS |
authorizer    | ------------------------------------------------------------------------------
authorizer    | Integration.Doubled Transaction                                       | PASS |
authorizer    | 1 critical test, 1 passed, 0 failed
authorizer    | 1 test total, 1 passed, 0 failed
authorizer    | ==============================================================================
authorizer    | Integration.High Frequency Small Interval
authorizer    | ==============================================================================
authorizer    | Check Output                                                          | PASS |
authorizer    | ------------------------------------------------------------------------------
authorizer    | Integration.High Frequency Small Interval                             | PASS |
authorizer    | 1 critical test, 1 passed, 0 failed
authorizer    | 1 test total, 1 passed, 0 failed
authorizer    | ==============================================================================
authorizer    | Integration.Insufficient Limit
authorizer    | ==============================================================================
authorizer    | Check Output                                                          | PASS |
authorizer    | ------------------------------------------------------------------------------
authorizer    | Integration.Insufficient Limit                                        | PASS |
authorizer    | 1 critical test, 1 passed, 0 failed
authorizer    | 1 test total, 1 passed, 0 failed
authorizer    | ==============================================================================
authorizer    | Integration.Regular Transaction
authorizer    | ==============================================================================
authorizer    | Check Output                                                          | PASS |
authorizer    | ------------------------------------------------------------------------------
authorizer    | Integration.Regular Transaction                                       | PASS |
authorizer    | 1 critical test, 1 passed, 0 failed
authorizer    | 1 test total, 1 passed, 0 failed
authorizer    | ==============================================================================
authorizer    | Integration                                                           | PASS |
authorizer    | 7 critical tests, 7 passed, 0 failed
authorizer    | 7 tests total, 7 passed, 0 failed
authorizer    | ==============================================================================
authorizer    | Output:  /tests/reports/integration/output.xml
authorizer    | Log:     /tests/reports/integration/log.html
authorizer    | Report:  /tests/reports/integration/report.html
authorizer    | All done, goodbye
authorizer exited with code 0
```

The test reports for the unit tests are saved under the ```tests/reports/unit/YYYY-MM-DD_HHMMSS.html```
file and the coverage report for the unit tests under ```tests/reports/unit/coverage/index.html```.

The test reports for the system (integration) tests are saved under the ```tests/reports/integration/```
directory, both ```report.html``` and ```log.html``` files.

## Structure

Here is how the project is structured:

* **/app**: Interfaces, classes, application starting point and the file containing the operations to be processed
* **/tests**: Unit and integration (system) tests and reports
* **/resources**: Configuration files and tooling scripts

## Thanks

That's all folks!
