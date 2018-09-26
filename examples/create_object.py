# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 NII.
#
# invenio-iiif-manifest is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

import os
from uuid import uuid4

from invenio_db import InvenioDB, db
from invenio_files_rest.models import ObjectVersion
from invenio_pidstore.providers.recordid import RecordIdProvider
from invenio_records import Record
from invenio_records_files.api import Record as RecordFile
from invenio_records_files.models import RecordsBuckets


def create_files_object(bucket, files_dict):
    files_meta = []
    iiif_files = 0
    iiif_adaptable_ext = ['.jpg','.jpeg','.png','.gif','.tif','tiff']

    for file_dict in files_dict:
        file_path = file_dict['path']
        file_name = os.path.basename(file_path)
        root, ext = os.path.splitext(file_path)

        if ext.lower() in iiif_adaptable_ext:
            iiif_files += 1

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
    return files_meta, iiif_files


def create_object(bucket, record_dict):
    """Object creation inside the bucket using the file and its content."""

    rec_uuid = uuid4()
    provider = RecordIdProvider.create(object_type='rec', object_uuid=rec_uuid)

    files, iiif_files = create_files_object(bucket, record_dict['_files'])

    iiif_manifest_url = ''
    if iiif_files > 0:
        iiif_manifest_url = '/record/{0}/iiif/manifest.json'.format(
            provider.pid.pid_value
        )

    deposit_dict = record_dict['_deposit']
    deposit_dict['iiif_manifest'] = iiif_manifest_url
    #deposit = str(deposit_dict)


    data = {
        'pid_value': provider.pid.pid_value,
        '_deposit': deposit_dict,
        '_files': files,
    }

    # from invenio_records_files.api import Record as RecordFile
    record = RecordFile.create(data, id_=rec_uuid)

    # connect to record and bucket
    db.session.add(RecordsBuckets(
        record_id=record.id,
        bucket_id=bucket.id,
    ))
    db.session.commit()
