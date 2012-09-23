from pages.models import Visit

class CountUserMiddleware(object):

	def process_request(self, request):
		Visit.objects.get_or_create(ip=request.META['REMOTE_ADDR'])