from imagekit.specs import ImageSpec
from imagekit import processors


class ResizePostThumb(processors.Resize):
	height = 150
	width = 150

class ResizePostMedium(processors.Resize):
	height = 300
	width = 300
	
class PostThumb(ImageSpec):
	processors = [ResizePostThumb]
	access_as = 'thumb'
	
class PostMedium(ImageSpec):
	processors = [ResizePostMedium]
	access_as = 'medium'