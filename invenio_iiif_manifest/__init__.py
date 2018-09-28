# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that adds more fun to the platform."""

from __future__ import absolute_import, print_function

from .ext import InvenioIIIFManifest
from .version import __version__
from . import restful

__all__ = ('__version__', 'InvenioIIIFManifest')
