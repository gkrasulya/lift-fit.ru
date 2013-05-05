from imagekit.specs import ImageSpec
from imagekit import processors


class ResizeSpareThumb(processors.Resize):
	height = 300
	width = 300
	crop = True


class ResizeSpareThumbCarousel(processors.Resize):
	height = 100
	width = 120
	crop = True


class ResizeSpareThumbCatalog(processors.Resize):
	height = 160
	width = 160
	crop = True
	
	
class SpareThumb(ImageSpec):
	processors = [ResizeSpareThumb]
	access_as = 'thumb'

	
class SpareThumbCarousel(ImageSpec):
	processors = [ResizeSpareThumbCarousel]
	access_as = 'thumb_carousel'

	
class SpareThumbCatalog(ImageSpec):
	processors = [ResizeSpareThumbCatalog]
	access_as = 'thumb_catalog'