from invenio_files_rest.models import Bucket, Location, ObjectVersion
from invenio_pidstore.models import PersistentIdentifier
from invenio_records.models import RecordMetadata

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///../example_app/test.db',echo=False)
Session = sessionmaker(bind=engine)
session = Session()

def pid2record_json(pid):
    """get record json from pid"""

    uuid = session.query(
        PersistentIdentifier.object_uuid).filter_by(pid_value=pid)[0][0]

    json = session.query(
        RecordMetadata.json).filter_by(id=uuid)[0][0]
    return json


def key2iiif_identifier(key):
    """get iiif_identifier to key"""

    ideitifier = str(session.query(ObjectVersion).filter_by(key=key)[0])
    return ideitifier


def pid2iiif_ideitifier(pid):
    """get iiif identifier from pid"""

    json = pid2record_json(pid)

    identifiers = []
    keys = json['files'].keys()
    for key in keys:
        identifiers.append(key2iiif_identifier(key))
    return identifiers
