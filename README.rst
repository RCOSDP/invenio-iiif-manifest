..
    Copyright (C) 2018 NII.
    invenio-iiif-manifest is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

=======================
 invenio-iiif-manifest
=======================

.. image:: https://img.shields.io/travis/inveniosoftware/invenio-iiif-manifest.svg
        :target: https://travis-ci.com/RCOSDP/invenio-iiif-manifest

.. image:: https://img.shields.io/coveralls/inveniosoftware/invenio-iiif-manifest.svg
        :target: https://coveralls.io/r/inveniosoftware/invenio-iiif-manifest

.. image:: https://img.shields.io/github/tag/inveniosoftware/invenio-iiif-manifest.svg
        :target: https://github.com/RCOSDP/invenio-iiif-manifest/releases

.. image:: https://img.shields.io/pypi/dm/invenio-iiif-manifest.svg
        :target: https://pypi.python.org/pypi/invenio-iiif-manifest

.. image:: https://img.shields.io/github/license/inveniosoftware/invenio-iiif-manifest.svg
        :target: https://github.com/RCOSDP/invenio-iiif-manifest/blob/master/LICENSE

Invenio module for generating iiif manifest par a record on invenio.

If user upload some image files to Invenio, the module automatically generate IIIF presentation manifest JSON file. Accessing bellow API, user can get the manifest.


http(s)://{example.com}/record/{record_id}/iiif/manifest.json


By passing the manifest to the IIIF viewer such as Mirador, it is possible to preview the image files on the record.


This module depends on invenio-iiif as it needs to access IIIF Image API.
