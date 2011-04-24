from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

from forms import *
from models import *

def page(request, slug):
	"""simple text page"""
	page = Page.objects.get(slug=slug)
	
	return render(request, 'pages/page.html', {
		'page': page
	})

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
	})

def feedback_thanks(request):
	return render(request, 'pages/feedback_thanks.html')
	
def site_map(request):
	return render(request, 'pages/site_map.html')

@csrf_exempt
def read_action(request, message_id):
	message = Message.objects.get(pk=message_id)

	message.read = not message.read
	message.save()

	return HttpResponse('Ok')
