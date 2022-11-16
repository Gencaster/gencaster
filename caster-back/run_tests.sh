#!/bin/sh

export SUPERCOLLIDER_HOST=127.0.0.1
export SUPERCOLLIDER_PORT=57120

cd "$(dirname "$0")"

echo "Check for necessary dependencies"
pip install --quiet -r requirements-test.txt

echo "Run mypy tests"
mypy .

echo "Run unit tests with coverage"
coverage run --source='.' manage.py test --settings=gencaster.settings.test -v 2

echo "Create coverage report"
coverage html --directory='coverage'
coverage xml
