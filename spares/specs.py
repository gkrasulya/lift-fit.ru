from imagekit.specs import ImageSpec
from imagekit import processors


class ResizeSpareDisplay(processors.Resize):
	width = 200
	
	
class SpareDisplay(ImageSpec):
	processors = [ResizeSpareDisplay]