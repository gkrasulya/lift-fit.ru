# -*- encoding: utf-8 -*- 

import re

from django import forms
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template import Template, Context
from django.template.loader import get_template

from models import *

class RegisterForm(forms.Form):
	email = forms.EmailField(_(u'Email'), required=True)
	password = forms.CharField(_(u'Пароль'), required=True, widget=forms.PasswordInput)

	def clean(self):
		data = super(RegisterForm, self).clean()

		try:
			User.objects.filter(username=data.get('email'))[0]
			raise forms.ValidationError(u'Пользователь с таким email уже зарегистрирован')
		except IndexError:
			pass

		return data

	def clean_password(self):
		data = self.data

		if len(data['password']) < 6:
			raise forms.ValidationError(u'Пароль слишком короткий (минимум 6 симоволов)')

		return data

	def save(self, *args, **kwargs):
		data = self.data
		user = User(email=data['email'], username=data['email'])
		user.set_password(data['password'])
		user.save()

class AuthForm(forms.Form):
	email = forms.EmailField(label=_(u'Email'), required=True)
	password = forms.CharField(label=_(u'Пароль'), required=True, widget=forms.PasswordInput)

	def clean(self):
		data = super(AuthForm, self).clean()
		user = authenticate(username=data.get('email'), password=data.get('password'))

		if user is None:
			raise forms.ValidationError(u'Неправильный email или пароль')

		return data

class EditForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		exclude = ('user',)