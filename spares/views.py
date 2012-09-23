from urllib import urlencode

from django.views.generic.list_detail import object_detail, object_list
from django.shortcuts import redirect, get_object_or_404, render
from django.core.urlresolvers import reverse

from models import *

def index(request):
	return render(request, 'index.html', {
		'slug': 'catalog'
	})

def producer_detail_redirect(request, id):
	producer = get_object_or_404(Producer, pk=id)
	query = urlencode(request.GET)
	redirect_url = '{0}?{1}'.format(reverse('spares-producer-detail', args=[producer.slug, producer.id]), query)
	# raise Exception, redirect_url
	return redirect(redirect_url, permanent=True)

def producer_detail(request, slug, id):
	category = request.GET.get('category', 'all')

	spare_list = Spare.objects.filter(producer=id)
	if category != 'all':
		spare_list = spare_list.filter(category=category)
	producer = Producer.objects.get(pk=id)
	extra_context = {
		'spare_list': spare_list,
		'catalog': True,
		'producer': producer,
		'category': category,
	}
	return object_detail(request, Producer.objects.all(), object_id=id,
		extra_context=extra_context, template_object_name='producer')