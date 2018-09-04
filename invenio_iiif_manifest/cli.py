# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

import sys
from models import pid2iiif_ideitifier
from models import pid2record_json
from iiif_manifest import invenioIIIFManifest

if __name__ == "__main__":
    argv = sys.argv
    pid = int(argv[1])
    if pid > 0:
        identifiers = pid2iiif_ideitifier(pid)
        #print(pid2record_json(pid))
        manifest = invenioIIIFManifest()
        manifest.add_metadata('label','foo','en')
        for identifier in identifiers:
            manifest.add_canvas(identifier)

        manifest.generate_manifest()
