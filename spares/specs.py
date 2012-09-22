from imagekit.specs import ImageSpec
from imagekit import processors


class ResizeSpareThumb(processors.Resize):
	height = 150
	width = 150
	
	
class SpareThumb(ImageSpec):
	processors = [ResizeSpareThumb]
	access_as = 'thumb'