# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

import os
from uuid import uuid4

from flask_iiif import IIIF_FORMATS
from invenio_db import InvenioDB, db
from invenio_files_rest.models import ObjectVersion
from invenio_pidstore.providers.recordid import RecordIdProvider
from invenio_records import Record
from invenio_records_files.api import Record as RecordFile
from invenio_records_files.models import RecordsBuckets


# This files code should be replace, if invenio-records module become formal
# version.

def generate_files_metadata(bucket, files_dict):
    """Generator of files metadata on record metadata."""

    files_meta = []
    num_of_iiif_valid_files = 0
    # Supported ext: gif, jpeg, jpg, pdf, png, tif
    # If you want to add any extention, you have to customize flask-iiif module.
    iiif_adaptable_ext = [k for k, v in IIIF_FORMATS.items()]

    for file_dict in files_dict:
        file_path = file_dict['path']
        file_name = os.path.basename(file_path)
        ext = os.path.splitext(file_path)[1][1:].lower()

        if ext in iiif_adaptable_ext:
            num_of_iiif_valid_files += 1

        with open(file_path, 'rb') as stream:
            obj = ObjectVersion.create(bucket, file_name, stream=stream)

            files_meta.append(
                {
                    'uri': '/files/{0}/{1}'.format(str(bucket.id), file_name),
                    'key': file_name,
                    'bucket': str(bucket.id),
                    'size': obj.file.size,
                    'version_id': str(obj.version_id),
                    'local': True,
                    'previewer': file_dict['previewer'],
                }
            )
    return files_meta, iiif_valid_files


def create_object(bucket, record_dict):
    """Object creation inside the bucket using the file and its content."""

    rec_uuid = uuid4()
    provider = RecordIdProvider.create(object_type='rec', object_uuid=rec_uuid)

    files_meta, num_of_iiif_valid_files = generate_files_metadata(
        bucket, record_dict['_files']
    )

    # If there are any iiif valid image files, iiif manifest api is added on
    # record metadata.
    iiif_manifest_url = ''
    if num_of_iiif_valid_files > 0:
        iiif_manifest_url = '/record/{0}/iiif/manifest.json'.format(
            provider.pid.pid_value
        )
    deposit_dict = record_dict['_deposit']
    deposit_dict['iiif_manifest'] = iiif_manifest_url

    data = {
        'pid_value': provider.pid.pid_value,
        '_deposit': deposit_dict,
        '_files': files_meta,
    }

    # from invenio_records_files.api import Record as RecordFile
    record = RecordFile.create(data, id_=rec_uuid)

    # connect to record and bucket
    db.session.add(RecordsBuckets(
        record_id=record.id,
        bucket_id=bucket.id,
    ))
    db.session.commit()
