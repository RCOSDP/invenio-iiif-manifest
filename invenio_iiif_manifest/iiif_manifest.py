# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

from .prezi_ext import ManifestFactory
import json
import glob

from . import config


class invenioIIIFManifest():
	'''generate iiif manifest for a record.'''

	def __init__(self,label='No Title'):
		self.factory = ManifestFactory()
		self.factory.set_base_prezi_uri(config.IIIF_MANIFEST_IMAGE_API_SERVER)
		self.factory.set_base_image_uri(config.IIIF_MANIFEST_IMAGE_API_BASE_URI)
		self.factory.set_iiif_image_info(version=config.IIIF_MANIFEST_IMAGE_API_VERSION, lvl=config.IIIF_MANIFEST_IMAGE_API_COMPLIAN)
		self.factory.set_debug("warn")
		self.manifest = self.factory.manifest(ident='identifier/manifest',label=label)
		self.manifest.viewingDirection = "left-to-right"
		self.metadata = MultiLanguageMetadata()
		self.page = 1
		self.sequence = None

	def set_description(self, description):
		self.manifest.description = str(description)

	def set_viewing_direction(self, direcsion):
		if direcsion in ['left-to-right','right-to-left','top-to-bottom','bottom-to-top']:
			self.manifest.viewingDirection = direcsion

	def add_metadata(self, key, value, language):
		self.metadata.add_meta(key, value, language)

	def generate_manifest(self):
		if self.metadata != None:
			self.manifest.set_metadata(self.metadata.export())

			return self.manifest.toJSON(top=True)

	def add_canvas(self, identifier):
		if self.sequence == None:
			self.sequence = self.manifest.sequence()

		canvas = self.sequence.canvas(ident="page-%s" % str(self.page), label="Page %s" % str(self.page))

		canvas_anno = canvas.annotation()
		img = canvas_anno.image(identifier, iiif=True)
		img.set_hw_from_iiif()

		canvas.height = img.height
		canvas.width = img.width
		self.page += 1

class MultiLanguageMetadata():
	'''generate multi language metadata for iiif manifest.'''

	def __init__(self):
		self.label = []
		self.value = []

	def add_meta(self,key,value,lang):
		self.add_label(key,lang)
		self.add_value(value,lang)

	def add_label(self, at_value, at_lang):
		self.label.append({"@value": at_value, "@language": at_lang})

	def add_value(self, at_value, at_lang):
		self.value.append({"@value": at_value, "@language": at_lang})

	def export(self):
		return self._generate_metadata()

	def _generate_metadata(self):
		metadata = {}
		metadata["label"] = self.label
		metadata["value"] = self.value
		return metadata


class SequentialManifestGenerator():
	'''generate iiif manifest depending on sequential image objects.'''

	def __init__(self, sequence):
		self.sequence = sequence
		self.page = 0;

	def _add_image_annotation(self, canvas, imagefile):
		annotation = canvas.annotation()

		image = annotation.image("p%s" % self.page, iiif=True, extention="png")

		image.set_hw_from_file(imagefile)

		canvas.height = image.height
		canvas.width = image.width

	def add_image(self, imagefile):
		'''add image to IIIF canvas'''

		self.page +=1
		canvas = self.sequence.canvas(ident="page-%s" % self.page, label="Page %s" % self.page)

		self._add_image_annotation(canvas, imagefile)



class InvenioIIIFSequentialManifestGenerator(SequentialManifestGenerator):

	def _add_image_annotation(self, canvas, file_obj):
		annotation = canvas.annotation()

		ui_iiif_image_url(file_obj)
		image = annotation.image(identifier, iiif=True)

		image.set_hw_from_file(imagefile)
		canvas.height = image.height
		canvas.width = image.width

	def add_image(self, file_obj):
		'''add image to IIIF canvas'''

		self.page +=1
		canvas = self.sequence.canvas(ident="page-%s" % self.page, label="Page %s" % self.page)

		self._add_image_annotation(canvas, file_obj)
