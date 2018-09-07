# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that adds more fun to the platform."""


INVENIO_IIIF_MANIFEST_BASE_TEMPLATE = 'invenio_iiif_manifest/base.html'
"""Default base template for the demo page."""


IIIF_MANIFEST_IMAGE_API_SERVER = 'http://localhost:5000/'
IIIF_MANIFEST_IMAGE_API_PREFIX = 'iiif/v2/'
IIIF_MANIFEST_IMAGE_API_VERSION = 2.0
IIIF_MANIFEST_IMAGE_API_COMPLIAN = 2
IIIF_MANIFEST_IMAGE_API_BASE_URI = IIIF_MANIFEST_IMAGE_API_SERVER + IIIF_MANIFEST_IMAGE_API_PREFIX
IIIF_MANIFEST_ADAPTABLE_EXT = ['.jpg','.jpeg','.png','.gif','.tif','tiff']

IIIF_MANIFEST_REST_ENDPOINTS = {

}


RECORDS_UI_ENDPOINTS = {
    'recid_iiif_manifest': {
        'pid_type': 'recid',
        'route': '/record/<pid_value>/iiif/manifest.json',
        'view_imp': 'invenio_iiif_manifest.restful.manifest_json',
        'record_class': 'invenio_records_files.api:Record'
    },
}
"""Records UI for invenio-iiif-manifest."""
