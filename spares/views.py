from django.views.generic.list_detail import object_detail, object_list

from models import *

def producer_detail(request, producer_id):
	spare_list = Spare.objects.filter(producer=producer_id)
	extra_context = {
		'spare_list': spare_list,
		'catalog': True,
	}
	return object_detail(request, Producer.objects.all(), object_id=producer_id,
		extra_context=extra_context, template_object_name='producer')