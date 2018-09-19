# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Generator for IIIF Presentation API's manifest."""

from . import config
from .prezi_ext import ManifestFactory


class InvenioIIIFManifestGenerator(object):
    """generate IIIF Presentation API manifest for a record."""

    def __init__(self, label="No Title"):
        """Initializer."""
        self.factory = ManifestFactory()
        self.factory.set_base_prezi_uri(
            config.IIIF_MANIFEST_IMAGE_API_SERVER
        )
        self.factory.set_base_image_uri(
            config.IIIF_MANIFEST_IMAGE_API_BASE_URI
        )
        self.factory.set_iiif_image_info(
            version=config.IIIF_MANIFEST_IMAGE_API_VERSION,
            lvl=config.IIIF_MANIFEST_IMAGE_API_COMPLIAN
        )

        # 'warn' will print warnings, default level
        # 'error' will turn off warnings
        # 'error_on_warning' will make warnings into errors

        self.factory.set_debug("error")
        self.manifest = self.factory.manifest(
            ident="identifier/manifest",
            label=label
        )
        self.manifest.viewingDirection = "left-to-right"
        self.metadata = MultiLanguageMetadata()
        self.page = 1
        self.sequence = None

    def description(self, description):
        """Setter description."""
        self.manifest.description = str(description)

    def viewing_direction(self, direcsion):
        """Setter viewing direction."""
        direcsions = [
            "left-to-right",
            "right-to-left",
            "top-to-bottom",
            "bottom-to-top"
        ]
        if direcsion in direcsions:
            self.manifest.viewingDirection = direcsion

    def multi_lang_metadata(self, key, value, language):
        """Setter multi language metadata."""
        self.metadata.add_meta(key, value, language)

    def generate_manifest(self):
        """Getter IIIF Presentation's manifest."""
        if self.metadata is not None:
            self.manifest.set_metadata(self.metadata.export())

            return self.manifest.toJSON(top=True)

    def add_canvas(self, identifier):
        """Create canvas."""
        if self.sequence is None:
            self.sequence = self.manifest.sequence()

        canvas = self.sequence.canvas(ident="page-%s" % str(self.page),
                                      label="Page %s" % str(self.page)
                                      )

        canvas_anno = canvas.annotation()
        img = canvas_anno.image(identifier, iiif=True, extension="png")
        img.set_hw_from_iiif()

        canvas.height = img.height
        canvas.width = img.width
        self.page += 1


class MultiLanguageMetadata(object):
    """Generate multi language metadata for iiif manifest."""

    def __init__(self):
        """Initializer."""
        self.label = []
        self.value = []

    def add_meta(self, key, value, lang):
        """Setter for metadata."""
        self._add_label(key, lang)
        self._add_value(value, lang)

    def export(self):
        """Getter for metadata."""
        return self._generate_metadata()

    def _add_label(self, at_value, at_lang):
        self.label.append({"@value": at_value, "@language": at_lang})

    def _add_value(self, at_value, at_lang):
        self.value.append({"@value": at_value, "@language": at_lang})

    def _generate_metadata(self):
        metadata = {}
        metadata["label"] = self.label
        metadata["value"] = self.value
        return metadata
