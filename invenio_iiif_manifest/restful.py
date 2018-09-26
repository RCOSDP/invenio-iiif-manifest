# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that adds more fun to the platform."""


from flask import abort, jsonify

from .api import can_generate, generate_iiif_manifest


def manifest_json(pid, record, template=None, **kwargs):
    """Render a iiif manifest json from record metadata."""
    files = record.dumps()["_files"]
    record_meta = record.dumps()["_deposit"]

    if can_generate(files):
        return jsonify(generate_iiif_manifest(pid, record_meta, files))
    else:
        abort(404)
