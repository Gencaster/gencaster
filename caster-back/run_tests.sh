#!/bin/sh

export SUPERCOLLIDER_HOST=localhost
export SUPERCOLLIDER_PORT=57120

cd "$(dirname "$0")"

COVERAGE_OMIT='*__init__*,*wsgi*,*urls*,*settings*,*/migrations/*,*/tests.py,*admin*,*apps.py,*manage.py,osc_server.py'

echo "Check for necessary dependencies"
pip install --quiet -r requirements-test.txt

echo "Run mypy tests"
mypy

echo "Run unit tests with coverage"
coverage run --source='.' manage.py test --settings=gencaster.settings.test -v 2

echo "Create coverage report"
coverage html --directory='coverage'
coverage xml
