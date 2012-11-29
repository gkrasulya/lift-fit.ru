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

ORDER_SEND_EMAIL = getattr(settings, 'ORDER_SEND_EMAIL', True)
ORDER_EMAILS = getattr(settings, 'ORDER_EMAILS', 'gkrasulya@gmail.com')
EMAIL_HOST_USER = getattr(settings, 'EMAIL_HOST_USER', 'feedback@lift-fit.ru')

class RegisterForm(forms.Form):
	email = forms.EmailField(_(u'Email'), required=True)
	password = forms.CharField(_(u'Пароль'), label=u'Пароль', required=True, widget=forms.PasswordInput)
	get_emails = forms.BooleanField(_(u'Получать рассылку'), label=u'Получать рассылку', initial=True, help_text=u'Возможность получения дополнительных скидок, участие в акциях, получение каталогов компании с продаваемой продукцией и прайс-листов, а также многое другое.')
	name = forms.CharField(_(u'Имя'), label=u'Имя', required=False)

	def clean(self):
		data = super(RegisterForm, self).clean()

		try:
			User.objects.filter(username=data.get('email'))[0]
			raise forms.ValidationError(u'Пользователь с таким email уже зарегистрирован')
		except IndexError:
			pass

		return data

	def clean_name(self):
		data = self.data

		if data['name'] != '':
			raise forms.ValidationError(u'Неправильное значение')

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
		profile = UserProfile(user=user)
		profile.get_emails = data['get_emails']
		profile.save()


class AuthForm(forms.Form):
	email = forms.EmailField(label=_(u'Email'), required=True)
	password = forms.CharField(label=_(u'Пароль'), required=True, widget=forms.PasswordInput)

	def clean(self):
		data = super(AuthForm, self).clean()
		user = authenticate(username=data.get('email'), password=data.get('password'))

		if user is None:
			raise forms.ValidationError(u'Неправильный email или пароль')

		return data


class RestorePasswordForm(forms.Form):
	email = forms.EmailField(label=_(u'Email'), required=True)

	def clean(self):
		data = super(RestorePasswordForm, self).clean()

		try:
			self.user = User.objects.filter(username=data.get('email'))[0]
		except IndexError:
			raise forms.ValidationError(u'Пользователя с таким email не существует')

		return data

	def save(self):
		send_restore_email(self.user.email, self.user.password)


class ChangePasswordForm(forms.Form):
	password = forms.CharField(label=_(u'Пароль'), required=True, widget=forms.PasswordInput)
	password_confirmation = forms.CharField(label=_(u'Подтверждение пароля'), required=True, widget=forms.PasswordInput)

	def clean(self):
		data = super(ChangePasswordForm, self).clean()
		if data.get('password') != data.get('password_confirmation'):
			raise forms.ValidationError(u'Пароли не совпадают')

		if len(data.get('password')) < 6:
			raise forms.ValidationError(u'Пароль слишком короткий')

		return data

	def save(self, request):
		request.user.set_password(self.cleaned_data['password'])
		request.user.save()


class EditForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		exclude = ('user',)


def send_restore_email(email, token):
	email_from = EMAIL_HOST_USER
	ctx = Context({
		'token': token
	})
	body = get_template('spares/restore_password_email.eml').render(ctx)

	email = EmailMessage(_(u'Обратная связь'), body, email_from, [email])
	email.send(fail_silently=False)