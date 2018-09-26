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
pip install -e ..

# Preapare all static files:
npm install -g node-sass clean-css clean-css-cli requirejs uglify-js
flask npm
cd static ; npm install ; cd ..

mkdir -p static/scss/invenio_search_ui
touch static/scss/invenio_search_ui/search.scss
mkdir -p static/js/invenio_deposit
touch static/js/invenio_deposit/app.js
mkdir -p static/js/invenio_search_ui
touch static/js/invenio_search_ui/app.js

flask collect -v
flask assets build

mkdir sample_files

if [ -e bucket ]; then
  rm -R bucket
fi
mkdir bucket

if [ -e test.db ]; then
  rm test.db
fi

if [ -e sample_files ]; then
  rm -R sample_files
fi
mkdir sample_files
cd sample_files
curl http://agora.ex.nii.ac.jp/digital-typhoon/kml/globe/latest/4.jpg -o jpgfile.jpg
curl https://www.nii.ac.jp/en/news/2017/12/20171225-02.png -o pngfile.png
cd ..

flask db init
flask db create
flask fixtures files
