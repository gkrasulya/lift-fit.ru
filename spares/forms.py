# -*- encoding: utf-8 -*- 

import re

from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.utils.translation import ugettext_lazy as _
from django.template import Template, Context
from django.template.loader import get_template

from models import *

ORDER_SEND_EMAIL = getattr(settings, 'ORDER_SEND_EMAIL', True)
ORDER_EMAILS = getattr(settings, 'ORDER_EMAILS', 'gkrasulya@gmail.com')
EMAIL_HOST_USER = getattr(settings, 'EMAIL_HOST_USER', 'feedback@lift-fit.ru')
FEEDBACK_EMAILS = getattr(settings, 'FEEDBACK_EMAILS', 'feedback@lift-fit.ru')

class OrderForm(forms.ModelForm):
	body = ''

	class Meta:
		model = Order
		exclude = ('date_added', 'read', 'status', 'body', 'total_sum', 'user')

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
		# order = super(OrderForm, self).save(*args, **kwargs)
		data = dict([(kw, val) for kw, val in self.data.iteritems() if hasattr(Order, kw)])
		order = Order(**data)
		send_order(order, customer_body=self.body)
		return order


class DeliveryForm(forms.ModelForm):
	class Meta:
		model = Delivery

	def save(self, *args, **kwargs):
		data = super(DeliveryForm, self).clean()
		delivery = super(DeliveryForm, self).save(*args, **kwargs)
		send_delivery(data.get('subject'), data.get('body'))
		return delivery


def send_delivery(subject, body):
	for user in User.objects.filter(get_emails=True):
		EmailMessage(subject, body, 'info@lift-fit.ru', [user.email]).send(fail_silently=False)
	

def send_order(order, customer_body, **kwargs):
	if ORDER_SEND_EMAIL or True:
		email_from = EMAIL_HOST_USER

		body = u'%s\n\nИмя: %s\nEmail: %s\nТелефон: %s\nКупон: %s\n\nВы' % (
			customer_body,
			order.name,
			order.email or u'нет',
			order.phone or u'нет',
			order.coupon or u'нет',
		)

		ctx = Context({
			'body': body
		})
		# body = get_template('spares/order_email.eml').render(ctx)

		email = EmailMessage(_(u'Обратная связь'), body, 'info@lift-fit.ru', FEEDBACK_EMAILS)
		email.send(fail_silently=False)

		customer_body = get_template('spares/order_email.eml').render(Context({
			'name': order.name,
			'body': customer_body,
		}))

		email = EmailMessage(_(u'Заказ на lift-fit.ru'), customer_body, 'info@lift-fit.ru', [order.email])
		email.content_subtype = 'html'
		email.send(fail_silently=False)