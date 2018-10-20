#!/bin/sh

# quit on errors:
set -o errexit

# quit on unbound symbols:
set -o nounset

DIR=`dirname "$0"`

cd $DIR
export FLASK_APP=app.py

# Setup fixtures
# Create sample files via internet
if [ -e sample_files ]; then
  rm -R sample_files
fi
mkdir sample_files
cd sample_files
curl http://agora.ex.nii.ac.jp/digital-typhoon/kml/globe/latest/4.jpg -o jpgfile.jpg
curl https://www.nii.ac.jp/en/news/2017/12/20171225-02.png -o pngfile.png
cd ..

# Create a user
flask users create info@inveniosoftware.org -a --password 123456

# Load some test data (you can re-run the command many times)
flask fixtures files
