from iiif_prezi.factory import ManifestFactory as _ManifestFactory
from iiif_prezi.factory import Annotation as _Annotation
from iiif_prezi.factory import Image as _Image
from iiif_prezi.factory import ImageService
'''This code was built for file's extention.'''


class ManifestFactory(_ManifestFactory):
    def annotation(self, ident="", label="", mdhash={}):
        """Create an Annotation."""
        if ident and not is_http_uri(ident):
            self.assert_base_prezi_uri()
        return Annotation(self, ident, label=label)

    def image(self, ident, label="", iiif=False, region='full', size='full', extention="jpg"):
        """Create an Image."""

        if not ident:
            raise RequirementError(
                "Images must have a real identity (Image['@id'] cannot be empty)")
        return Image(self, ident, label, iiif, region, size, extention=extention)


class Annotation(_Annotation):
    def image(self, ident="", label="", iiif=False, extention='jpg'):
        """Create Image body."""
        img = self._factory.image(ident, label, iiif, extention=extention)
        self.resource = img
        return img


class Image(_Image):
    def __init__(self, factory, ident, label, iiif=False, region='full', size='full',extention='jpg'):
        """Initialize Image resource."""
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

            if factory.default_image_api_version[0] == '1':
                self.id = factory.default_base_image_uri + '/' + \
                    ident + '/%s/%s/0/native.%s' % (region, size, extention)
            else:
                self.id = factory.default_base_image_uri + '/' + \
                    ident + '/%s/%s/0/default.%s' % (region, size, extention)
            self._identifier = ident
            self.format = mime_type[extention]
