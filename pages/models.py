# *-* coding: utf-8 *-*

import re

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

from imagekit.models import ImageModel
from fields import AutoImageField

class Page(models.Model):
	title = models.CharField(_(u'Заголовок'), max_length=255)
	text = models.TextField(_(u'Текст'), blank=True)
	text_html = models.TextField(_(u'Text html'), editable=False)
	name = models.CharField(_(u'Имя'), max_length=255)
	slug = models.SlugField(_(u'Слаг'), blank=True)
	date_added = models.DateTimeField(_(u'Дата добавления'), auto_now_add=True, editable=False)
	date_updated = models.DateTimeField(_(u'Дата добавления'), auto_now=True, editable=False)

	page_title = models.TextField(_(u'Название страницы'), blank=True, default='',
		help_text=_(u'то, что будет отображаться во вкладке браузера'))
	meta_keywords = models.TextField(_(u'Ключевые слова'), blank=True, default='',
		help_text=_(u'содержимое для &lt;meta name="keywords" /&gt;'))
	meta_description = models.TextField(_(u'Описание'), blank=True, default='',
		help_text=_(u'содержимое для &lt;meta name="description" /&gt;'))
	
	class Meta:
		verbose_name = _(u'Страница')
		verbose_name_plural = _(u'Страницы')
		
	def save(self, force_insert=False, force_update=False):
		self.text_html = format_text(self.text)
		super(Page, self).save(force_insert, force_update)

	def __unicode__(self):
		return self.name

	def get_page_title(self):
		return self.page_title if self.page_title else self.title


class Post(ImageModel):
	title = models.CharField(_(u'Заголовок'), max_length=255)
	photo = AutoImageField(upload_to='photos', verbose_name=_(u'Фото'), blank=True)
	text = models.TextField(_(u'Текст'), blank=True)
	text_html = models.TextField(_(u'Text html'), editable=False)
	slug = models.SlugField(_(u'Слаг'), blank=True)
	date_added = models.DateTimeField(_(u'Дата добавления'), auto_now_add=True, editable=False)
	date_updated = models.DateTimeField(_(u'Дата добавления'), auto_now=True, editable=False)

	page_title = models.TextField(_(u'Название страницы'), blank=True, default='',
		help_text=_(u'то, что будет отображаться во вкладке браузера'))
	meta_keywords = models.TextField(_(u'Ключевые слова'), blank=True, default='',
		help_text=_(u'содержимое для &lt;meta name="keywords" /&gt;'))
	meta_description = models.TextField(_(u'Описание'), blank=True, default='',
		help_text=_(u'содержимое для &lt;meta name="description" /&gt;'))
	
	class Meta:
		verbose_name = _(u'Новость')
		verbose_name_plural = _(u'Новости')

	class IKOptions:
		spec_module  = 'pages.specs'
		image_field = 'photo'
		
	def save(self, force_insert=False, force_update=False):
		self.text_html = format_text(self.text)
		super(Post, self).save(force_insert, force_update)

	def __unicode__(self):
		return self.title
		
	def get_absolute_url(self):
		return reverse('pages-post-detail', args=(self.slug, self.id))

	def get_page_title(self):
		return self.page_title if self.page_title else self.title


class Message(models.Model):
	CATEGORIES = (
		('order', u'Заказ запчастей'),
		('delivery', u'Запрос на поставку оборудования'),
		('service', u'Запрос на техническое  обслуживание'),
		('installation', u'Запрос на монтаж оборудования'),
		('advice', u'Пожелания и предложения'),
	)

	name = models.CharField(_(u'Ваше имя'), max_length=255)
	email = models.EmailField(_(u'E-mail'), max_length=255, blank=True,
		help_text=_(u'Нужно для ответа на письмо'))
	phone = models.CharField(_(u'Телефон'), max_length=255, blank=True)
	body = models.TextField(_(u'Сообщение'))
	category = models.CharField(_(u'Категория'), choices=CATEGORIES, max_length=255, blank=False)
	read = models.BooleanField(_(u'"прочитано"'), default=False)
	date_added = models.DateTimeField(_(u'"добавлено"'), auto_now_add=True, editable=False)

	class Meta:
		verbose_name = _(u'Сообщение')
		verbose_name_plural = _(u'Сообщения')
		ordering = ['-date_added', '-id']

	def __unicode__(self):
		return '%s, %s' % (
			self.date_added.strftime('%Y.%m.%d'),
			self.name
		)

	def read_helper(self):
		return '<a href="" class="read-action" id="readAction%s">%s</a>' % (
			self.id, u'Отметить непрочитанным' if self.read else u'Отметить прочитанным')
	read_helper.short_description = u'Действия'
	read_helper.allow_tags = True

	def admin_files(self):
		files_count = self.files.count()
		if files_count:
			return u'<a href="/admin/pages/messagefile/?message=%s">Прикрепленных файлов: %s</a>' % (
				self.id,
				files_count,
			)
		return _(u'Нет')
	admin_files.allow_tags = True
	admin_files.short_description = _(u'Прикрепленные файлы')


class Visit(models.Model):
	ip = models.IPAddressField()
	date_added = models.DateTimeField(_(u'"добавлено"'), auto_now_add=True, editable=False)

	class Meta:
		verbose_name = _(u'Визит')
		verbose_name_plural = _(u'Визиты')
		ordering = ['-id']

class MessageFile(models.Model):
	IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif')

	message = models.ForeignKey(Message, related_name='files')
	attachment = models.FileField(upload_to='attachments')
	date_added = models.DateTimeField(_(u'Добавлено'), auto_now_add=True, editable=False)

	class Meta:
		verbose_name = _(u'Файл сообщения')
		verbose_name_plural = _(u'Файлы сообщения')
		ordering = ['-id']

	def name(self):
		return self.attachment.name.rsplit('/', 1)[1]
	name.short_description = _(u'Имя файла')

	def admin_preview(self):
		name = self.name()
		if name and name.rsplit('.', 1)[1] in self.IMAGE_EXTENSIONS:
			preview = '<img src="%s" style="max-height: 200px; max-width: 200px;" />' % self.attachment.url
		else:
			preview = name
		return '<a href="%s">%s</a>' % (self.attachment.url, preview)
	admin_preview.short_description = _(u'Файл')
	admin_preview.allow_tags = True

	def admin_message(self):
		return '<a href="/admin/pages/message/?id=%s">%s</a>' % (
			self.message.id,
			self.message
		)
	admin_message.short_description = _(u'Сообщение')
	admin_message.allow_tags = True


def format_text(text=None):
	if text is None:
		return ''
		
	text = re.sub(r'\n\n', '</p>\n\n<p>', text)
	text = re.sub(r'\n', '<br/>', text)
	
	return text
