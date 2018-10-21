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

    return app_


@pytest.yield_fixture()
def app(base_app):
    """Flask application fixture."""
    Babel(base_app)
    InvenioAccounts(base_app)
    InvenioAccess(base_app)
    InvenioDB(base_app)
    InvenioFilesREST(base_app)
    InvenioREST(base_app)
    InvenioIIIFAPI(base_app)
    InvenioIIIFManifest(base_app)

    with base_app.app_context():
        yield base_app


@pytest.fixture()
def images_meta1():
    """Image files metadata set."""
    metadata = [
        {
            "bucket": "object_bucket",
            "version_id": "object_version",
            "key": "jpgfile.jpg",
            "previewer": ""
        },
        {
            "bucket": "object_bucket",
            "version_id": "object_version",
            "key": "pngfile.png",
            "previewer": ""
        }
    ]
    return metadata


@pytest.fixture()
def images_meta2():
    """Image files metadata set."""
    metadata = [
        {
            "bucket": "object_bucket",
            "version_id": "object_version",
            "key": "jpgfile.jpg",
            "previewer": ""
        },
        {
            "bucket": "object_bucket",
            "version_id": "object_version",
            "key": "example.docx",
            "previewer": ""
        }
    ]
    return metadata


@pytest.fixture()
def docx_meta():
    """Non-image files metadata set."""
    metadata = [
        {
            "bucket": "object_bucket",
            "version_id": "object_version",
            "key": "sample1.docx",
            "previewer": ""
        },
        {
            "bucket": "object_bucket",
            "version_id": "object_version",
            "key": "sample2.docx",
            "previewer": ""
        }
    ]
    return metadata


@pytest.fixture()
def docx_meta():
    """Non-image files metadata set."""
    metadata = [
        {
            "bucket": "object_bucket",
            "version_id": "object_version",
            "key": "sample1.docx",
            "previewer": ""
        },
        {
            "bucket": "object_bucket",
            "version_id": "object_version",
            "key": "sample2.docx",
            "previewer": ""
        }
    ]
    return metadata


@pytest.fixture()
def record_meta():
    """record metadata set."""
    metadata = {
        "title": "IIIF test record",
        "description": "This is test record.",
    }
    return metadata


@pytest.fixture()
def image_path():
    """Image file path."""
    return "sample.png"


@pytest.fixture()
def docx_path():
    """Not image file path."""
    return "sample.docx"


@pytest.fixture()
def pid():
    """PID object."""
    class pid(object):
        pid_value = 1

    return pid
