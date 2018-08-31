from .models import pid2iiif_ideitifier
from .iiif_manifest import invenioIIIFManifest



def generate_iiif_manifest(pid):
	'''generate iiif manifest from image files on the target record from pid'''

    #identifiers = pid2iiif_ideitifier(pid)
	identifiers = ['c22878fe-de33-41cf-917a-418307c26f79:6780eb7f-ec36-4369-974c-37797c011a4c:mars_map_sample.png']
	manifest = invenioIIIFManifest()
	manifest.add_metadata('label','foo','en')
	for identifier in identifiers:
		manifest.add_canvas(identifier)

	return manifest.generate_manifest()
