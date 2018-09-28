# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Extension of iiif-prezi module.

The iiif-prezi module can not indicate image format of IIIF Image API.
The module export only jpg format such as "defalt.jpg".
This source code can indicate other image format like png and tif, etc.

Attention: Should be indicate formats that IIIF Image API server can deliver.

There is no function which can export a manifest file with Image API on for
IIIF Presentation API IIIF.

iiif-prezi detail
-----------------

https://github.com/iiif-prezi/iiif-prezi
"""

from iiif_prezi.factory import Annotation as _Annotation
from iiif_prezi.factory import Image as _Image
from iiif_prezi.factory import ImageService
from iiif_prezi.factory import ManifestFactory as _ManifestFactory


class ManifestFactory(_ManifestFactory):
    """This code is extention purpose."""

    def annotation(self, ident="", label="", mdhash={}):
        """This code is extention purpose."""
        if ident and not is_http_uri(ident):
            self.assert_base_prezi_uri()
        return Annotation(self, ident, label=label)

    def image(self, ident, label="", iiif=False, region="full",
              size="full", extension="jpg"):
        """This code is extention purpose."""
        if not ident:
            raise RequirementError(
                ("Images must have a real identity (Image['@id'] cannot"
                 "be empty)")
                )
        return Image(self, ident, label, iiif, region, size,
                     extension=extension)


class Annotation(_Annotation):
    """This code is extention purpose."""

    def image(self, ident="", label="", iiif=False, extension="jpg"):
        """Create Image body."""
        img = self._factory.image(ident, label, iiif, extension=extension)
        self.resource = img
        return img


class Image(_Image):
    """This code is extention purpose."""

    def __init__(self, factory, ident, label, iiif=False, region="full",
                 size="full", extension="jpg"):
        """This code is extention purpose."""
        self._factory = factory
        self.type = self.__class__._type
        self.label = ""
        self.format = ""
        self.height = 0
        self.width = 0
        self._identifier = ""

        mime_type = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png"
        }

        if label:
            self.set_label(label)

        if iiif:
            # add IIIF service -- iiif is version or bool
            # ident is identifier
            self.service = ImageService(factory, ident)

            if factory.default_image_api_version[0] == "1":
                self.id = factory.default_base_image_uri + "/" + \
                    ident + "/%s/%s/0/native.%s" % (region, size, extension)
            else:
                self.id = factory.default_base_image_uri + "/" + \
                    ident + "/%s/%s/0/default.%s" % (region, size, extension)
            self._identifier = ident
            self.format = mime_type[extension]
