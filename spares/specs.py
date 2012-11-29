from imagekit.specs import ImageSpec
from imagekit import processors


class ResizeSpareThumb(processors.Resize):
	height = 200
	width = 200
	
	
class SpareThumb(ImageSpec):
	processors = [ResizeSpareThumb]
	access_as = 'thumb'