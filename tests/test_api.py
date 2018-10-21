# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""API tests."""

from flask import Flask

from invenio_iiif_manifest import InvenioIIIFManifest
from invenio_iiif_manifest.api import can_generate, can_preview, \
    generate_identifier_for_invenio_iiif, generate_identifier_pid_key, \
    generate_iiif_manifest


def test_can_generate(app, images_meta1, images_meta2, docx_meta):
    """Test metada with image files."""
    assert can_generate(images_meta1) is True
    assert can_generate(images_meta2) is True
    assert can_generate(docx_meta) is False


def test_can_preview(app, image_path, docx_path):
    """Test iiif image file."""
    assert can_preview(image_path) is True
    assert can_preview(docx_path) is False


def test_generate_identifier_pid_key(app, images_meta1, pid):
    """Test flask-iiif identifier."""
    identifier = generate_identifier_pid_key(pid(), images_meta1[0])
    assert identifier == "1:jpgfile.jpg"


def test_generate_identifier_for_invenio_iiif(app, images_meta1):
    """Test flask-iiif identifier."""

    identifier = generate_identifier_for_invenio_iiif(images_meta1[0])
    assert identifier == "object_bucket:object_version:jpgfile.jpg"


# If you want to below test, you have to do "flask run" and remove comments
# out.
# def test_generate_iiif_manifest(app, pid1_meta_on_db):
#     """Test iiif manifest"""
#     record_meta = pid1_meta_on_db['_deposit']
#     images_meta = pid1_meta_on_db['_files']
#     pid = 1
#     generate_iiif_manifest(pid, record_meta, images_meta)
