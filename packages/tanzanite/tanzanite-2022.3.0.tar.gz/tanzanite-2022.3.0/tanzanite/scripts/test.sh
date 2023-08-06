#! /usr/bin/env bash

# Exit in case of error
set -e

# Ensure stack is removed on exit.
function on_exit()
{
    docker-compose -f docker-stack.yml down -v --remove-orphans
}
trap on_exit EXIT SIGHUP SIGINT SIGQUIT SIGTERM


DOMAIN=backend \
SMTP_HOST="" \
TRAEFIK_PUBLIC_NETWORK_IS_EXTERNAL=false \
INSTALL_DEV=true \
docker-compose \
    -f docker-compose.yml \
    config > docker-stack.yml

docker-compose -f docker-stack.yml build
docker-compose -f docker-stack.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-stack.yml up -d
docker-compose -f docker-stack.yml exec -T backend bash /app/tests-start.sh "$@" 2>&1
