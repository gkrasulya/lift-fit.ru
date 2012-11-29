# -*- encoding: utf-8 -*- 

import json
from urllib import urlencode

from django.http import HttpResponse
from django.views.generic.list_detail import object_detail, object_list
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.template.loader import get_template
from django.views.decorators.http import require_POST

from models import *
from forms import OrderForm

def index(request):
	return render(request, 'index.html', {
		'slug': 'catalog',
	})

@csrf_exempt
def manage_cart(request):
	return _manage_products(request, 'cart')

@csrf_exempt
def manage_favorites(request):
	if request.user.is_anonymous():
		response = HttpResponse('{"ok":false}')
		response.status_code = 400
		return response


	id = request.POST.get('id', None)
	add = request.POST.get('add', True)

	if id is None:
		response = HttpResponse('{"ok":false}')
		response.status_code = 400
		return response
	id = int(id)

	try:
		request.user.favorite_list.filter(id=id)
	except ObjectDoesNotExist:
		response = HttpResponse('{"ok":false}')
		response.status_code = 400
		return response

	spare = Spare.objects.filter(id=id)[0]
	if add == 'true':
		request.user.favorite_list.add(spare)
	else:
		request.user.favorite_list.remove(spare)
	request.user.save()

	response = HttpResponse(json.dumps({
		'ok': True	
	}))

	if add == 'true':
		product_ids = _get_product_ids_from_cookies(request, 'cart')
		if id in product_ids:
			product_ids.remove(id)
			response.set_cookie('cart_ids', json.dumps(product_ids), max_age=86400*7, path='/')
	return response


def _manage_products(request, name):
	id = request.POST.get('id', None)
	add = request.POST.get('add', True)
	if id is None:
		response = HttpResponse('{"ok":false}')
		response.status_code = 400
		return response
	id = int(id)

	if not request.user.is_anonymous() and add == 'true':
		spare = Spare.objects.filter(id=id)[0]
		request.user.favorite_list.remove(spare)
		request.user.save()

	product_ids = _get_product_ids_from_cookies(request, name)
	if add == 'true' and id not in product_ids:
		product_ids.append(id)
	elif id in product_ids:
		product_ids.remove(id)

	response = HttpResponse('{"ok":true}');
	response.set_cookie('%s_ids' % name, json.dumps(product_ids), max_age=86400*7, path='/')
	return response

def producer_detail_redirect(request, id):
	producer = get_object_or_404(Producer, pk=id)
	query = urlencode(request.GET)
	redirect_url = '{0}?{1}'.format(reverse('spares-producer-detail', args=[producer.slug, producer.id]), query)
	return redirect(redirect_url, permanent=True)

def producer_detail(request, slug, id):
	category = request.GET.get('category', 'all')
	current_rank = request.GET.get('rank', None)
	# category_type = request.GET.get('')

	spare_list = Spare.objects.filter(producer=id)
	if current_rank is not None:
		spare_list = spare_list.filter(rank__in=(current_rank, ''))
	if category != 'all':
		spare_list = spare_list.filter(category=category)
	producer = Producer.objects.get(pk=id)

	cart_ids = _get_product_ids_from_cookies(request, 'cart')
	if cart_ids:
		for spare in spare_list:
			if spare.id in cart_ids:
				spare.in_cart = True

	if not request.user.is_anonymous():
		favorite_list = request.user.favorite_list.all()
		for spare in spare_list:
			if spare in favorite_list:
				spare.in_favorites = True

	extra_context = {
		'spare_list': spare_list,
		'catalog': True,
		'producer': producer,
		'category': category,
		'current_producer': producer,
		'ranks': Spare.RANKS,
		'current_rank': int(current_rank) if current_rank is not None else None,
	}
	return object_detail(request, Producer.objects.all(), object_id=id,
		extra_context=extra_context, template_object_name='producer')

def cart(request):
	cart_ids = _get_product_ids_from_cookies(request, 'cart')
	spare_list = Spare.objects.filter(id__in=cart_ids)

	return render(request, 'spares/cart.html', {
		'spare_list': spare_list
	})

@require_POST
def order(request):
	product_ids = [int(x) for x in request.POST.getlist('products')]
	quantities = [int(x) for x in request.POST.getlist('quantities')]
	spare_list = Spare.objects.filter(id__in=product_ids)
	is_order = request.POST.has_key('_order')
	order_products = []
	body = []
	total_sum = 0
	for i, spare in enumerate(spare_list):
		body.append(u'%s - %s\n шт.' % (spare.title, quantities[i]))
		total_sum += spare.price * quantities[i]
		order_products.append({
			'spare': spare,
			'quantity': quantities[i]
		})
	body = '\n'.join(body)

	data = request.POST.copy() if is_order else None
	if data is not None:
		data['body'] = body
		data['total_sum'] = total_sum
		if not request.user.is_anonymous():
			data['user_id'] = request.user.id
	else:
		if is_order:
			pass
			# raise Exception('DATA IS NONE')

	if request.user.is_anonymous():
		form = OrderForm(data)
	else:
		try:
			profile = request.user.profile
			form = OrderForm(data, instance=profile, initial={'email': request.user.email})
		except:
			form = OrderForm(data)

	if is_order and form.is_valid():
		form.save()
		response = render(request, 'spares/success.html', {

		})
		response.set_cookie('cart_ids', json.dumps([]))
		return response
	else:
		return render(request, 'spares/form.html', {
			'order_products': order_products,
			'form': form,
			'is_order': is_order,
			'total_sum': total_sum
		})

def get_cart(request):
	cart_ids = _get_product_ids_from_cookies(request, 'cart')
	spare_list = Spare.objects.filter(id__in=cart_ids).all()

	total_price = 0
	for spare in spare_list:
		total_price += spare.price

	ctx = Context({
		'total_count': len(spare_list),
		'total_price': total_price
	})
	t = get_template('spares/_cart.html').render(ctx)

	response = HttpResponse(json.dumps({
		'ok': True,
		'html': t
	}))
	return response

def _get_product_ids_from_cookies(request, name):
	cart_ids = request.COOKIES.get('%s_ids' % name, None)
	if cart_ids is not None:
		cart_ids = json.loads(cart_ids)
	else:
		cart_ids = []
	return cart_ids