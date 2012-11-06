import json
from urllib import urlencode

from django.http import HttpResponse
from django.views.generic.list_detail import object_detail, object_list
from django.shortcuts import redirect, get_object_or_404, render
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as logout_, authenticate, login as login_
from django.contrib.auth.decorators import login_required
from django.template import Template, Context
from django.template.loader import get_template
from django.views.decorators.http import require_POST

from forms import *

import logging
logger = logging.getLogger(__name__)

import sys

def register(request):
	form = RegisterForm(request.POST if request.method == 'POST' else None)

	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('/account/edit/')
	
	return render(request, 'account/register.html', {
		'form': form
	})

def login(request):
	form = AuthForm(request.POST if request.method == 'POST' else None)

	if request.method == 'POST':
		if form.is_valid():
			user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
			login_(request, user)
			return redirect(request.GET.get('next', '/account/'))

	return render(request, 'account/login.html', {
		'form': form
	})

def logout(request):
	logout_(request)
	return redirect('/')

@login_required
def account(request):
	order_list = request.user.order_list.order_by('-id').all()

	return render(request, 'account/account.html', {
		'order_list': order_list,
		'current_tab': 'account',
	})

@login_required
def favorites(request):
	favorite_list = request.user.favorite_list.all()

	return render(request, 'account/favorites.html', {
		'favorite_list': favorite_list,
		'current_tab': 'favorites',
	})

@login_required
def edit(request):
	try:
		profile = request.user.profile
	except:
		profile = UserProfile.objects.create(user=request.user)

	form = EditForm(request.POST if request.method == 'POST' else None, instance=profile)

	if request.method == 'POST':
		if form.is_valid():
			form.save()

	return render(request, 'account/edit.html', {
		'form': form,
		'current_tab': 'edit',
	})