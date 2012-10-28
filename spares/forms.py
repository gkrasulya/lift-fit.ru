# -*- encoding: utf-8 -*- 

import re

from django import forms
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.utils.translation import ugettext_lazy as _
from django.template import Template, Context
from django.template.loader import get_template

from models import *

ORDER_SEND_EMAIL = getattr(settings, 'ORDER_SEND_EMAIL', True)
ORDER_EMAILS = getattr(settings, 'ORDER_EMAILS', 'gkrasulya@gmail.com')
EMAIL_HOST_USER = getattr(settings, 'EMAIL_HOST_USER', 'feedback@lift-fit.ru')

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		exclude = ('date_added', 'read', 'status', 'body', 'total_sum')

	def clean_coupon(self):
		data = self.cleaned_data['coupon']

		if data.strip():
			try:
				coupon = Coupon.objects.filter(coupon=data)[0]
				coupon.activated = True
				coupon.save()
			except IndexError:
				raise forms.ValidationError(_(u'Вы ввели неверный купон'))

		return data

	def save(self, *args, **kwargs):
		order = super(OrderForm, self).save(*args, **kwargs)
		send_order(order)
	

def send_order(order, **kwargs):
	if ORDER_SEND_EMAIL:
		email_from = EMAIL_HOST_USER

		body = u'%s\n\nИмя: %s\n\nEmail: %s\n\nТелефон: %s' % (
			order.body,
			order.name,
			order.email or u'нет',
			order.phone or u'нет',
		)

		if message.email:
			email_from = message.email

		ctx = Context({
			'body': body
		})
		body = get_template('spares/order_email.eml').render(ctx)

		email = EmailMessage(_(u'Обратная связь'), body, 'info@lift-fit.ru', FEEDBACK_EMAILS)
		email.send(fail_silently=False)