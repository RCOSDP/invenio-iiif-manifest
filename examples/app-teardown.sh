#!/bin/sh

# quit on errors:
set -o errexit

# quit on unbound symbols:
set -o nounset

DIR=`dirname "$0"`

cd $DIR
export FLASK_APP=app.py

# Teardown app
[ -e "$DIR/instance" ] && rm -Rf $DIR/instance

if [ -e bucket ]; then
  rm -R bucket
fi

if [ -e static ]; then
  rm -R static
fi

if [ -e test.db ]; then
  rm test.db
fi
