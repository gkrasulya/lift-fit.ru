from imagekit.specs import ImageSpec
from imagekit import processors


class ResizeSpareThumb(processors.Resize):
	height = 300
	width = 300
	crop = True
	
	
class SpareThumb(ImageSpec):
	processors = [ResizeSpareThumb]
	access_as = 'thumb'