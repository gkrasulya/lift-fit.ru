#-*- coding: utf-8 -*- 
import re

from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ImageModel
from fields import AutoImageField


class UserProfile(models.Model):
	name = models.CharField(u'Имя', help_text=u'ФИО полностью', max_length=255, blank=True)
	phone = models.CharField(u'Телефон', max_length=50, blank=True)
	address = models.TextField(u'Адрес', blank=True)
	user = models.OneToOneField(User, related_name='profile')