# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

import os

from .models import pid2iiif_ideitifier
from .iiif_manifest import invenioIIIFManifest
from . import config

def can_generate(files):
	for file in files:
		root, ext = os.path.splitext(file['key'])

		if ext.lower() in config.IIIF_MANIFEST_ADAPTABLE_EXT:
			return True

	return False


def generate_iiif_manifest(pid, files):
	'''generate iiif manifest from image files on the target record from pid'''

	identifiers = []
	#files = record.dumps()['_files']
	for file in files:
		identifier = ':'.join([file['bucket'], file['version_id'], file['key']])
		identifiers.append(identifier)

	manifest = invenioIIIFManifest('PID: ' + pid.pid_value)
	manifest.add_metadata('pid',str(pid),'en')
	manifest.set_description('This collection is automatically genarated from Invenio.')
	manifest.set_viewing_direction('left-to-right')
	for identifier in identifiers:
		manifest.add_canvas(identifier)
	return manifest.generate_manifest()
