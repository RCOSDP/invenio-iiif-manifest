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
from invenio_rest import ContentNegotiatedMethodView
from flask import current_app, request, url_for, jsonify

blueprint = Blueprint(
    'invenio_iiif_manifest',
    __name__,
    template_folder='templates',
    static_folder='static',
)

@blueprint.route("/record/<string:pid>/iiif/manifest.json")
def index(pid):
    """Render a basic view."""

    result = {
        "Result":{
        "pid": pid
        }
    }

    return jsonify(ResultSet=result)
