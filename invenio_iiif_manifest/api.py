from .models import pid2iiif_ideitifier
from .iiif_manifest import invenioIIIFManifest


def generate_iiif_manifest(pid, record):
	'''generate iiif manifest from image files on the target record from pid'''

	identifiers = []
	files = record.dumps()['_files']
	for file in files:
		identifier = ':'.join([file['bucket'], file['version_id'], file['key']])
		identifiers.append(identifier)
	#identifiers = ['f104e734-1934-439f-9750-f9770451d0ca:14890973-6d34-4721-8b0a-fa304ebc5f13:mars_map_sample.png']
	manifest = invenioIIIFManifest('PID: '+pid.pid_value)
	manifest.add_metadata('pid',str(pid),'en')
	manifest.set_description('This collection is automatically genarated from Invenio.')
	manifest.set_viewing_direction('left-to-right')
	for identifier in identifiers:
		manifest.add_canvas(identifier)
	return manifest.generate_manifest()
