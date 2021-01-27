#!/usr/bin/env bash
#
# @file      entrypoint.sh
# @author    Me :-)
# @version   0.0.1
# @brief     Docker container entrypoint
#
# Leaves if any command fails
set -e

# Used for debugging if no foreground application is being called
# while true; do
#     date
#     sleep 5
# done

# Call the application in foreground, in test mode, just run the unit tests,
# generate test and coverage reports and exit
if [ ${APP_TEST_MODE} = "True" ]; then
    echo "Starting the unit tests"
    /usr/bin/env python -m pytest -vv --cov=. --cov-report html:/tests/reports/unit/coverage --html=/tests/reports/unit/$(date +%Y-%m-%d_%H%M%S).html /tests/unit/

    echo "Starting the integration tests"
    /usr/bin/env python -m robot -d /tests/reports/integration /tests/integration/

    echo "All done, goodbye"
else
    ./authorizer.py < operations
fi
