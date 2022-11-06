#!/bin/sh

python manage.py export_schema "gencaster.schema" > "schema.gql"
