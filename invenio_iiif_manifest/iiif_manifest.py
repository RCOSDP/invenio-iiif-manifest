#from iiif_prezi.factory import ManifestFactory
from prezi_ext import ManifestFactory
import json
import glob
from invenio_iiif.utils import ui_iiif_image_url

from api import MultiLanguageMetadata
from api import SequentialManifestGenerator


class invenioIIIFManifest():
	image_api_server = 'http://localhost:5000/'
	image_api_prefix = 'iiif/v2/'
	manifest_output = './output/'
	image_api_version = 2.0
	image_api_complian = 2

	def __init__(self):
		self.factory = ManifestFactory()

		self.factory.set_base_prezi_uri(self.image_api_server)

		api_base_url = self.image_api_server+self.image_api_prefix
		self.factory.set_base_image_uri(api_base_url)

		self.factory.set_base_prezi_dir("./output/")
		self.factory.set_iiif_image_info(self.image_api_version, self.image_api_complian)
		self.factory.set_debug("warn")
		self.manifest = self.factory.manifest(ident='manifest',label="Example Manifest")
		self.manifest.viewingDirection = "left-to-right"
		self.metadata = MultiLanguageMetadata()
		self.page = 1
		self.sequence = None

	def set_description(self, description):
		self.manifest.description = str(description)

	def set_viewing_direction(self, direcsion):
		self.manifest.viewingDirection = direcsion

	def add_metadata(self, key, value, language):
		self.metadata.add_meta(key, value, language)

	def generate_manifest(self):
		if self.metadata != None:
			self.manifest.set_metadata(self.metadata.export())

			self.manifest.toFile(compact=False)

	def add_canvas(self, identifier):
		if self.sequence == None:
			self.sequence = self.manifest.sequence()

		canvas = self.sequence.canvas(ident="page-%s" % str(self.page), label="Page %s" % str(self.page))

		anno = canvas.annotation()
		img = anno.image(identifier, iiif=True)
		img.set_hw_from_iiif()

		canvas.height = img.height
		canvas.width = img.width
		self.page += 1
