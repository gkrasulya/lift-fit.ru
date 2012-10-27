#-*- coding: utf-8 -*- 
import re

from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ImageModel
from fields import AutoImageField

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ['fields.AutoImageField'])


class Producer(models.Model):
	"""Producer"""
	title = models.CharField(_(u'Название'), max_length=255, blank=True)
	date_added = models.DateTimeField(_(u'Date added'), auto_now_add=True, editable=False)
	date_updated = models.DateTimeField(_(u'Date updated'), auto_now=True, editable=False)
	
	text = models.TextField(_(u'Текст'), blank=True)
	text_html = models.TextField(_(u'Text html'), editable=False)
	slug = models.SlugField(_(u'Слаг'), blank=True)

	split_into_categories = models.BooleanField(_(u'Делить на категории'), default=False)

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
		
	def save(self, force_insert=False, force_update=False):
		self.text_html = format_text(self.text)
		super(Producer, self).save(force_insert, force_update)
		
	def get_absolute_url(self):
		return reverse('spares-producer-detail', args=(self.slug, self.id))

	def get_page_title(self):
		return self.page_title if self.page_title else self.title


class Spare(ImageModel):
	CATEGORIES = (
		(u'elevator', u'Лифт'),
		(u'escalator', u'Эскалатор'),
	)

	RANKS = (
		(0,  u'Станция управленя'),
		(1,  u'Привод лифта'),
		(2,  u'Шахта лифта'),
		(3,  u'Кабина лифта'),
		(4,  u'Электрооборудование'),
		(5,  u'Гидравлика'),
		(6,  u'Привод эскалатора'),
		(7,  u'Балюстрада'),
		(8,  u'Входная площадка'),
		(9,  u'Ступени'),
		(10, u'Прочее'),
	)

	title = models.CharField(_(u'Название'), max_length=255)
	price = models.IntegerField(_(u'Цена'), max_length=25, default=0, null=False)
	description = models.TextField(_(u'Описание'), blank=True, default='', editable=False)
	description_html = models.TextField(_(u'Описание HMTL'), editable=False)
	photo = AutoImageField(upload_to='photos', verbose_name=_(u'Фото'))
	producer = models.ForeignKey(Producer, verbose_name=_(u'Производитель'))
	in_stock = models.BooleanField(u'В наличии')
	date_added = models.DateTimeField(_(u'Date added'), auto_now_add=True, editable=False)
	date_updated = models.DateTimeField(_(u'Date updated'), auto_now=True, editable=False)

	category = models.CharField(_(u'Категория'), max_length=50,
								choices=CATEGORIES, blank=True, null=True)
	rank = models.CharField(_(u'Ранжировка'), max_length=50,
								choices=RANKS, blank=True, default='', db_column='type_')
	user_list = models.ManyToManyField(User, related_name='favorite_list')

	in_cart = False
	
	class Meta:
		ordering = ['title']
		verbose_name = _(u'Запчасть')
		verbose_name_plural = _(u'Запчасти')

	class IKOptions:
		spec_module  = 'spares.specs'
		image_field = 'photo'
	
	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return '%s#spare%s' % (reverse('spares-producer-detail', args=[self.producer_id]), self.id)
		
	def save(self, force_insert=False, force_update=False):
		self.description_html = format_text(self.description)
		super(Spare, self).save(force_insert, force_update)

	def admin_photo(self):
		return '<img src="%s" />' % self.thumb.url
	admin_photo.short_description = _(u'Фото')
	admin_photo.allow_tags = True


class Order(models.Model):
	STATUSES = (
		(0, u'Заказ сформирован и отправлен поставщику'),
		(1, u'Заказ упакован и готов к отправке'),
		(2, u'Заказ отправлен на транзитный склад в Европе'),
		(3, u'Заказ поступил на транзитный склад'),
		(4, u'Заказ отправлен в Россию'),
		(5, u'Заказ поступил на таможню и проходит таможенную очистку'),
		(6, u'Заказ поступил на склад в Москве'),
		(7, u'Заказ отправлен в адрес Заказчика'),
		(8, u'Заказ получен Заказчиком'),
	)

	name = models.CharField(_(u'Имя'), max_length=255, help_text=u'ФИО полностью')
	email = models.EmailField(_(u'E-mail'), max_length=255, blank=False)
	phone = models.CharField(_(u'Телефон'), max_length=255, blank=False)
	address = models.TextField(_(u'Адре'), blank=False)
	body = models.TextField(_(u'Детали'))
	read = models.BooleanField(_(u'"прочитано"'), default=False)
	date_added = models.DateTimeField(_(u'"добавлено"'), auto_now_add=True, editable=False)
	status = models.CharField(u'Статус', choices=STATUSES, max_length=255)
	coupon = models.CharField(u'Купон', max_length=50, blank=True, default='')

	total_sum = models.IntegerField(u'Сумма', default=0)

	user = models.ForeignKey(User, related_name='order_list')

	class Meta:
		verbose_name = _(u'Заказ')
		verbose_name_plural = _(u'Заказы')
		ordering = ['-date_added', '-id']

	def get_body_html(self):
		return self.body.replace('\n', '<br>')

	def get_user(self):
		try:
			return self.user
		except DoesNotExist:
			return None

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


class Coupon(models.Model):
	coupon = models.CharField(_(u'Купон'), max_length=50, blank=False)
	activated = models.BooleanField(_(u'Активирован'), default=False)


def format_text(text=None):
	if text is None:
		return ''
		
	text = re.sub(r'\n\n', '</p>\n\n<p>', text)
	text = re.sub(r'\n', '<br/>', text)
	
	return text