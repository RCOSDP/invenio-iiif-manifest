#!/bin/sh

# quit on errors:
set -o errexit

# quit on unbound symbols:
set -o nounset

DIR=`dirname "$0"`

cd $DIR
export FLASK_APP=app.py

# Install specific dependencies
pip install -r requirements.txt
pip install -e ../invenio_iiif_manifest

# Preapare all static files:
npm install -g node-sass clean-css clean-css-cli requirejs uglify-js
flask npm
cd static ; npm install ; cd ..

flask collect -v
flask assets build

if [ -e bucket ]; then
  rm -R bucket
fi
mkdir bucket

if [ -e test.db ]; then
  rm test.db
fi

flask db init
flask db create
flask fixtures files

flask users create info@inveniosoftware.org --password 123456
flask users activate info@inveniosoftware.org
