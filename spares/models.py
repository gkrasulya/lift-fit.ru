#-*- coding: utf-8 -*- 
import re

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ImageModel
from fields import AutoImageField
from specs import SpareDisplay

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ['fields.AutoImageField'])

class Producer(models.Model):
	"""Producer"""
	title = models.CharField(_(u'Название'), max_length=255, blank=True)
	date_added = models.DateTimeField(_(u'Date added'), auto_now_add=True, editable=False)
	date_updated = models.DateTimeField(_(u'Date updated'), auto_now=True, editable=False)

	page_title = models.TextField(_(u'Название страницы'), blank=True, default='',
		help_text=_(u'то, что будет отображаться во вкладке браузера'))
	meta_keywords = models.TextField(_(u'Ключевые слова'), blank=True, default='',
		help_text=_(u'содержимое для &lt;meta name="keywords" /&gt;'))
	meta_description = models.TextField(_(u'Описание'), blank=True, default='',
		help_text=_(u'содержимое для &lt;meta name="description" /&gt;'))
	
	class Meta:
			ordering = ['-date_added']
			verbose_name = _(u'Производитель')
			verbose_name_plural = _(u'Производители')
	
	def __unicode__(self):
		"""docstring for __unicode__"""
		return self.title
		
	def get_absolute_url(self):
		return reverse('spares-producer-detail', args=(self.id,))

	def get_page_title(self):
		return self.page_title if self.page_title else self.title


class Spare(ImageModel):
	title = models.CharField(_(u'Название'), max_length=255)
	description = models.TextField(_(u'Описание'))
	description_html = models.TextField(_(u'Описание HMTL'), editable=False)
	photo = AutoImageField(upload_to='photos', verbose_name=_(u'Фото'))
	producer = models.ForeignKey(Producer, verbose_name=_(u'Производитель'))
	date_added = models.DateTimeField(_(u'Date added'), auto_now_add=True, editable=False)
	date_updated = models.DateTimeField(_(u'Date updated'), auto_now=True, editable=False)
	
	class Meta:
		ordering = ['-date_added']
		verbose_name = _(u'Запчасть')
		verbose_name_plural = _(u'Запчасти')

	class IKOptions:
		preprocessor_spec = SpareDisplay
		image_field = 'photo'
	
	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return '%s#spare%s' % (reverse('spares-producer-detail', args=[self.producer_id]), self.id)
		
	def save(self, force_insert=False, force_update=False):
		self.description_html = format_text(self.description)
		super(Spare, self).save(force_insert, force_update)

	def admin_photo(self):
		return '<img src="%s" />' % self.photo.url
	admin_photo.short_description = _(u'Фото')
	admin_photo.allow_tags = True


def format_text(text=None):
	if text is None:
		return ''
		
	text = re.sub(r'\n\n', '</p>\n\n<p>', text)
	text = re.sub(r'\n', '<br/>', text)
	
	return text