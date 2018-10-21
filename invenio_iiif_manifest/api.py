# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""API for IIIF Presentation generation."""

from os.path import splitext

from flask import abort

from . import config
from .iiif_manifest import InvenioIIIFManifestGenerator


def can_generate(files):
    """Check if there are image files in a record."""
    for file in files:
        root, ext = splitext(file["key"])

        if ext.lower() in config.IIIF_MANIFEST_ADAPTABLE_EXT:
            return True

    return False


def can_preview(file_key):
    """Judge if file can preview."""
    root, ext = splitext(file_key)

    return ext.lower() in config.IIIF_MANIFEST_ADAPTABLE_EXT


def generate_identifier_pid_key(pid, file):
    """Generate IIIF identifier for 'pid:key'."""
    return ":".join([str(pid.pid_value), file["key"]])


def generate_identifier_for_invenio_iiif(file):
    """Generate IIIF identifier for 'bucket:version:key'.

    'bucket:version:key' is a setting required by invenio-iiif original
    settings.
    """
    return ":".join([file["bucket"], file["version_id"], file["key"]])


def generate_iiif_manifest(pid, record_meta, files):
    """Generate iiif manifest using IIIF Image API."""
    identifiers = []
    for file in files:
        if can_preview(file["key"]):
            if config.IIIF_MANIFEST_IMAGE_API_IDENTIFIER in ["default", None]:
                identifiers.append(
                    generate_identifier_for_invenio_iiif(file)
                )

            elif config.IIIF_MANIFEST_IMAGE_API_IDENTIFIER == "pid:key":
                identifiers.append(
                    generate_identifier_pid_key(pid, file)
                )

    if identifiers == []:
        abort(404)

    invenio_message = ("This iiif manifest json is generated via Invenio using"
                       "record metadata which has image files")

    manifest = InvenioIIIFManifestGenerator(record_meta["title"])
    manifest.description(record_meta["description"])
    manifest.multi_lang_metadata("system_message", invenio_message, "en")
    for identifier in identifiers:
        manifest.add_canvas(identifier)

    return manifest.generate_manifest()
