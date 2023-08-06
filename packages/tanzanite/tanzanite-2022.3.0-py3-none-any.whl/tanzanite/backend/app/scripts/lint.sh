#!/usr/bin/env bash

set -x

mypy app
pylint app
