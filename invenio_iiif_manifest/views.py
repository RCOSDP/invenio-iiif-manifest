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


def manifest_json(pid, record, template=None, **kwargs):
    """Render a basic view."""


    return jsonify(generate_iiif_manifest(pid, record))
