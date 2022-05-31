#!/bin/sh

export SUPERCOLLIDER_HOST=localhost
export SUPERCOLLIDER_PORT=57120

cd "$(dirname "$0")"

COVERAGE_OMIT='*__init__*,*wsgi*,*urls*,*settings*,*/migrations/*,*/tests.py,*admin*,*apps.py,*manage.py,osc_server.py'

pip install --quiet -r requirements-test.txt

coverage run --source='.' manage.py test --settings=gencaster.settings.test -v 2

coverage html --directory='coverage' --omit=$COVERAGE_OMIT

coverage xml
