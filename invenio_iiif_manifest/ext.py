# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that adds more fun to the platform."""

from . import config


class InvenioIIIFManifest(object):
    """invenio-iiif-manifest extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["invenio-iiif-manifest"] = self

    def init_config(self, app):
        """Initialize configuration."""
        if "BASE_TEMPLATE" in app.config:
            app.config.setdefault(
                "INVENIO_IIIF_MANIFEST_BASE_TEMPLATE",
                app.config["BASE_TEMPLATE"],
            )

        with_endpoints = app.config.get("RECORDS_UI_ENDPOINTS")
        for k in dir(config):
            if k.startswith("INVENIO_IIIF_MANIFEST_"):
                app.config.setdefault(k, getattr(config, k))

            else:
                for n in ["RECORDS_UI_ENDPOINTS"]:
                    if k == n and with_endpoints:
                        app.config.setdefault(n, {})
                        app.config[n].update(getattr(config, k))
