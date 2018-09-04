# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that adds more fun to the platform."""

from __future__ import absolute_import, print_function

from flask import Blueprint, render_template
from flask_babelex import gettext as _
from flask import current_app, request, url_for, jsonify

from .api import generate_iiif_manifest
from .api import can_generate


def manifest_json(pid, record, template=None, **kwargs):
    """Render a iiif manifest.json."""

    files = record.dumps()['_files']

    if can_generate(files):
        return jsonify(generate_iiif_manifest(pid, files))
    else:
        return jsonify({'err': 'can not generate iiif manifest becouse of no adaptable image files exist.'})
