class MultiLanguageMetadata():
	def __init__(self):
		self.label = []
		self.value = []

	def add_meta(self,key,value,lang):
		self.add_label(key,lang)
		self.add_value(value,lang)

	def add_label(self, at_value, at_lang):
		self.label.append({"@value": at_value, "@language": at_lang})

	def add_value(self, at_value, at_lang):
		self.value.append({"@value": at_value, "@language": at_lang})

	def export(self):
		#return json.dumps(self._generate_metadata(),indent=2)
		return self._generate_metadata()

	def _generate_metadata(self):
		metadata = {}
		metadata["label"] = self.label
		metadata["value"] = self.value
		return metadata


class SequentialManifestGenerator():
	def __init__(self, sequence):
		self.sequence = sequence
		self.page = 0;

	def _add_image_annotation(self, canvas, imagefile):
		annotation = canvas.annotation()

		import inspect
		#print(type(annotation))
		#print(inspect.getsource(annotation.image))
		image = annotation.image("p%s" % self.page, iiif=True, extention="png")

		image.set_hw_from_file(imagefile)
		#print(type(image))
		canvas.height = image.height
		canvas.width = image.width

	def add_image(self, imagefile):
		'''add image to IIIF canvas'''

		self.page +=1
		canvas = self.sequence.canvas(ident="page-%s" % self.page, label="Page %s" % self.page)

		self._add_image_annotation(canvas, imagefile)



class InvenioIIIFSequentialManifestGenerator(SequentialManifestGenerator):

	def _add_image_annotation(self, canvas, file_obj):
		annotation = canvas.annotation()

		#identifier = ":".join(file_obj.bucket, file_obj.version, file_obj.key)
		ui_iiif_image_url(file_obj)
		image = annotation.image(identifier, iiif=True)

		image.set_hw_from_file(imagefile)
		canvas.height = image.height
		canvas.width = image.width

	def add_image(self, file_obj):
		'''add image to IIIF canvas'''

		self.page +=1
		canvas = self.sequence.canvas(ident="page-%s" % self.page, label="Page %s" % self.page)

		self._add_image_annotation(canvas, file_obj)
		#print(file)
