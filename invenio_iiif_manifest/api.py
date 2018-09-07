# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

from os.path import splitext

from .models import pid2iiif_ideitifier
from .iiif_manifest import InvenioIIIFManifest
from . import config

def can_generate(files):
	"check if there are image files in a record"
	for file in files:
		root, ext = splitext(file['key'])

		if ext.lower() in config.IIIF_MANIFEST_ADAPTABLE_EXT:
			return True

	return False


def generate_iiif_manifest(pid, record_meta, files):
	'''generate iiif manifest from image files on the target record from pid'''

	identifiers = []
	for file in files:
		root, ext = splitext(file['key'])
		if ext.lower() in config.IIIF_MANIFEST_ADAPTABLE_EXT:
			identifier = ':'.join(
				[file['bucket'], file['version_id'], file['key']]
			)
			identifiers.append(identifier)

	manifest = InvenioIIIFManifest(record_meta['title'])
	manifest.description(record_meta['description'])
	manifest.multi_lang_metadata('system_message', 'This iiif manifest json is generated via Invenio using record metadata which has image files' ,'en')
	for identifier in identifiers:
		manifest.add_canvas(identifier)

	return manifest.generate_manifest()
