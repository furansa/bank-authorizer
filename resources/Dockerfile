#
# @file      Dockerfile
# @author    Me :-)
# @version   0.0.1
# @brief     Docker image build file
#
FROM python:3.8-slim

WORKDIR /app

COPY ./Pipfile /app/

ARG IMAGE_DESCRIPTION
LABEL Description=${IMAGE_DESCRIPTION}

# Update the system, create the app user and install the required packages
ARG PIP_OPTIONS
RUN apt-get update && apt-get upgrade -y && apt-get clean && \
useradd -d /app -M bank && \
pip3 install --upgrade pip && pip3 install pipenv && pipenv install ${PIP_OPTIONS}

# Run the application as unprivileged user for security reasons
USER bank

ENTRYPOINT ["/tmp/entrypoint.sh"]
