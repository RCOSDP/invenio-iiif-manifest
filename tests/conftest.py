# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration."""

import os
import shutil
import tempfile

import pytest
from flask import Flask
from flask_babelex import Babel
from invenio_access import InvenioAccess
from invenio_accounts import InvenioAccounts
from invenio_db import InvenioDB
from invenio_files_rest import InvenioFilesREST
from invenio_iiif import InvenioIIIFAPI
from invenio_records_rest.utils import PIDConverter
from invenio_rest import InvenioREST

from invenio_iiif_manifest import InvenioIIIFManifest


@pytest.yield_fixture()
def instance_path():
    """Temporary instance path."""
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


@pytest.fixture()
def base_app(instance_path):
    """Flask application fixture."""
    app_ = Flask('testapp', instance_path=instance_path)
    app_.url_map.converters['pid'] = PIDConverter
    app_.config.update(
        SECRET_KEY='SECRET_KEY',
        TESTING=True,
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

    Babel(app_)
    InvenioAccounts(app_)
    InvenioAccess(app_)
    InvenioDB(app_)
    InvenioFilesREST(app_)
    InvenioREST(app_)
    InvenioIIIFAPI(app_)
    InvenioIIIFManifest(app_)

    return app_


@pytest.yield_fixture()
def app(base_app):
    """Flask application fixture."""
    with base_app.app_context():
        yield base_app


@pytest.fixture()
def db_init(app):
    """Create records with data."""
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
