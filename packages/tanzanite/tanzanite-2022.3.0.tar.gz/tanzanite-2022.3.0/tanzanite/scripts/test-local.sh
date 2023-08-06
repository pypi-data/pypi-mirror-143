#! /usr/bin/env bash

# Exit in case of error
set -e

# Ensure stack is removed on exit.
function on_exit()
{
    docker-compose down -v --remove-orphans
}
trap on_exit EXIT SIGHUP SIGINT SIGQUIT SIGTERM


OS="$(uname -s)"
if [[ -z "${D2_SECRETS_BASEDIR}" ]]; then
    echo "D2_SECRETS_BASEDIR not defined"
	exit 1
fi
if [[ "${OS}" == "Linux" || "${OS}" == "Darwin" ]]; then
    echo "Remove __pycache__ files"
    find . -type d -name __pycache__ -exec rm -r {} \+
fi

docker-compose build
docker-compose up -d
docker-compose exec -T backend bash /app/tests-start.sh "$@" 2>&1
