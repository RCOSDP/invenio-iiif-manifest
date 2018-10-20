# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Minimal Flask application example.

SPHINX-START

First install invenio-iiif-manifest, setup the application and load
fixture data by running:

.. code-block:: console

   $ cd examples
   $ ./app-setup.sh
   $ ./app-fixtures.sh

Next, start the development server:

.. code-block:: console

   $ export FLASK_APP=app.py FLASK_DEBUG=1
   $ flask run

and open the example application in your browser:

.. code-block:: console

    $ open http://127.0.0.1:5000/

View iiif manifest in your browser::

    http://localhost:5000/record/1/iiif/manifest.json

To reset the example application run:

.. code-block:: console

    $ ./app-teardown.sh

SPHINX-END
"""


import json
import os
from os.path import dirname, join

from create_object import create_object
from flask import Flask
from invenio_access import InvenioAccess
from invenio_accounts import InvenioAccounts
from invenio_assets import InvenioAssets
from invenio_db import InvenioDB, db
from invenio_files_rest import InvenioFilesREST
from invenio_files_rest.models import Bucket, Location
from invenio_i18n import InvenioI18N
from invenio_iiif import InvenioIIIFAPI
from invenio_records import InvenioRecords, Record
from invenio_records_rest.utils import PIDConverter
from invenio_records_ui import InvenioRecordsUI
from invenio_records_ui.views import create_blueprint_from_app
from invenio_rest import InvenioREST
from invenio_theme import InvenioTheme

from invenio_iiif_manifest import InvenioIIIFManifest

# Create Flask application
app = Flask(__name__)

app.url_map.converters['pid'] = PIDConverter
app.config.update(
    SECRET_KEY='CHANGEME',
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    RECORDS_UI_DEFAULT_PERMISSION_FACTORY=None,
    RECORDS_UI_ENDPOINTS=dict(
        recid=dict(
            pid_type='recid',
            route='/record/<pid_value>',
            template='invenio_records_ui/detail.html',
        ),
        recid_files=dict(
            pid_type='recid',
            route='/record/<pid_value>/files/<path:filename>',
            view_imp='invenio_records_files.utils.file_download_ui',
            record_class='invenio_records_files.api:Record',
        ),
    ),
)


InvenioAccounts(app)
InvenioAccess(app)
InvenioAssets(app)
InvenioDB(app)
InvenioI18N(app)
InvenioTheme(app)
InvenioREST(app)
InvenioFilesREST(app)
InvenioRecords(app)
InvenioRecordsUI(app)
InvenioIIIFAPI(app)
InvenioIIIFManifest(app)

app.register_blueprint(create_blueprint_from_app(app))


@app.cli.group()
def fixtures():
    """Command for working with test data."""


@fixtures.command()
def files():
    """Load files."""
    bucket_path = os.path.join(os.path.dirname(__file__), 'bucket')

    if not os.path.isdir(bucket_path):
        os.makedirs(bucket_path)

    # Create location
    loc = Location(name='local', uri=bucket_path, default=True)
    db.session.add(loc)
    db.session.commit()

    # Bucket
    bucket = Bucket.create(location=loc)

    # Example files from the data folder
    with open('data/metadata.json') as file:
        example_records = json.load(file)['metadata']

        # Create records
        for record in example_records:
            create_object(bucket, record)
