# coding: utf-8

from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

from forms import *
from models import *
from spares.models import *

EMAIL_HOST_USER = getattr(settings, 'EMAIL_HOST_USER', 'feedback@lift-fit.ru')
FEEDBACK_EMAILS = getattr(settings, 'FEEDBACK_EMAILS', 'gkrasulya@gmail.com')

VISITS_COUNT_METRIKA = 2147

def index(request):
	page = Page.objects.get(slug='index')
	first_post = Post.objects.order_by('-date_added')[0]
	visits_count = Visit.objects.count() + VISITS_COUNT_METRIKA
	action_spares = Spare.objects.order_by('?')[:10]
	service_pages = Page.objects.filter(name='service')
	
	return render(request, 'pages/index.html', {
		'page': page,
		'main': True,
		'action_spares': action_spares,
		'first_post': first_post,
		'slug': 'index',
		'visits_count': visits_count,
		'visits_count_zfill': str(visits_count).zfill(4),
		'service_pages': service_pages,
	})

def english(request):
	visits_count = Visit.objects.count() + VISITS_COUNT_METRIKA

	return render(request, 'pages/english.html', {
		'visits_count': visits_count,
		'visits_count_zfill': str(visits_count).zfill(4),
		'slug': 'english'
	})

def service_detail(request, slug):
	"""simple text page"""
	page = Page.objects.get(slug=slug)

	template_name = 'service_detail'
	service_pages = Page.objects.filter(name='service')
	
	return render(request, 'pages/%s.html' % template_name, {
		'page': page,
		'slug': slug,
		'service_pages': service_pages,
	})

def page(request, slug):
	"""simple text page"""
	page = Page.objects.get(slug=slug)

	service_pages = None
	is_english = slug == 'english'

	template_name = 'page'
	if slug == 'usloviya-dostavki':
		template_name = 'delivery'
	elif slug == 'service':
		service_pages = Page.objects.filter(name='service')
		template_name = 'service'
	elif slug == 'about':
		template_name = 'about'
	
	return render(request, 'pages/%s.html' % template_name, {
		'page': page,
		'main': slug == 'index',
		'slug': slug,
		'service_pages': service_pages,
		'is_english': is_english
	})

def custom_page(request, slug):
	page = get_object_or_404(Page, slug=slug)

def post_list(request):
	posts = Post.objects.all()

	return render(request, 'pages/post_list.html', {
		'posts': posts	
	})

def post_detail(request, slug, id):
	post = Post.objects.get(id=id)

	return render(request, 'pages/post_detail.html', {
		'post': post
	})

def callback(request):

	if request.method == 'POST':
		email_from = EMAIL_HOST_USER

		body = u'Имя: %s\n\nТелефон: %s' % (
			request.POST.get('name'),
			request.POST.get('phone'),
		)

		email = EmailMessage(u'Обратный звонок', body, email_from, FEEDBACK_EMAILS)
		email.send(fail_silently=True)
	return HttpResponse('Ok')

def feedback(request):
	"""feedback page"""
	try:
		page = Page.objects.get(slug='feedback')
	except Page.DoesNotExist:
		page = None
		
	form = MessageForm(request.POST or None, request.FILES or None, auto_id='%s')
	if form.is_valid():
		form.save()
		if request.is_ajax():
			return HttpResponse('Ok')
		else:
			return redirect(reverse('pages-feedback-thanks'))

	if request.is_ajax():
		return HttpResponse('Error')
	
	return render(request, 'pages/feedback.html', {
		'form': form,
		'page': page,
		'slug': 'feedback'
	})

def feedback_thanks(request):
	return render(request, 'pages/feedback_thanks.html')
	
def site_map(request):
	return render(request, 'pages/site_map.html')
	
def site_map_xml(request):
	return render(request, 'pages/site_map.xml')
	
def robots_txt(request):
	return render(request, 'pages/robots.txt')

@csrf_exempt
def read_action(request, message_id):
	message = Message.objects.get(pk=message_id)

	message.read = not message.read
	message.save()

	return HttpResponse('Ok')
