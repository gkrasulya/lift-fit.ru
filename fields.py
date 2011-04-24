import os
import datetime
import time

from django.db.models import ImageField, signals

import settings

class AutoImageField(ImageField):
	
	def generate_filename(self, instance, filename):
		
		format = {
			'extension': filename.split('.')[-1],
			'time': '%d' % (time.time() * 100),
			'date': datetime.datetime.now().strftime('%Y-%m-%d'),
		}
		
		filename_format = '%(time)s.%(extension)s'	
		filename = filename_format % format
		
		return os.path.join(self.get_directory_name(), filename)