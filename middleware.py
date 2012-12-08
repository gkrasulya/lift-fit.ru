from django.core.exceptions import MultipleObjectsReturned

from pages.models import Visit

class CountUserMiddleware(object):

	def process_request(self, request):
		try:
			Visit.objects.get_or_create(ip=request.META['REMOTE_ADDR'])
		except MultipleObjectsReturned:
			pass