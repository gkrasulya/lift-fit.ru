# -*- encoding: utf-8 -*- 

import re

from django import forms
from django.core.mail import send_mail, EmailMessage
from django.utils.translation import ugettext_lazy as _

from models import *

FEEDBACK_SEND_EMAIL = getattr(settings, 'FEEDBACK_SEND_EMAIL', True)
FEEDBACK_EMAILS = getattr(settings, 'FEEDBACK_EMAILS', 'gkrasulya@gmail.com')
EMAIL_HOST_USER = getattr(settings, 'EMAIL_HOST_USER', 'feedback@lift-fit.ru')

class MessageForm(forms.ModelForm):
	
	class Meta:
		model = Message
		exclude = ('date_added', 'read',)

	def save(self, *args, **kwargs):
		message = super(MessageForm, self).save(*args, **kwargs)

		if self.files:
			for attachment in self.files.values():
					message_file = MessageFile(message=message)
					message_file.attachment.save(attachment.name, attachment)
					message_file.save()

		send_feedback(message)
	

def send_feedback(message, **kwargs):
	if FEEDBACK_SEND_EMAIL:
		email_from = EMAIL_HOST_USER

		body = u'%s\n\nИмя: %s\n\nEmail: %s\n\nТелефон: %s' % (
			message.body,
			message.name,
			message.email or u'нет',
			message.phone or u'нет',
		)

		if message.email:
			email_from = message.email

		email = EmailMessage(_(u'Обратная связь'), body, email_from, FEEDBACK_EMAILS)
		files = message.files.all()
		if files:
			for f in files:
				email.attach_file(f.attachment.path)
		email.send(fail_silently=False)