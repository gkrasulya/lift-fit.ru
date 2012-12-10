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
		(0, u'Лифт'),
		(1, u'Эскалатор'),
	)

	RANKS = (
		(u'Запчасти для лифтов', (
				(0,  u'Станция управления'),
				(1,  u'Привод лифта'),
				(2,  u'Шахта лифта'),
				(3,  u'Кабина лифта'),
				(4,  u'Электрооборудование'),
				(5,  u'Гидравлика'),
				(6, u'Прочее'),
			),
		),
		(u'Запчасти для эскалаторов', (
				(7,  u'Станция управленя'),
				(8,  u'Привод эскалатора'),
				(9,  u'Балюстрада'),
				(10,  u'Входная площадка'),
				(11,  u'Ступени'),
				(12, u'Прочее'),
			),
		),
	)

	SPECIAL_TYPES = (
		('action', u'Акция'),
		('recommend', u'Рекомендуем'),
		('special', u'Специальное предложение'),
	)

	title = models.CharField(_(u'Название'), max_length=255)
	price = models.IntegerField(_(u'Цена'), max_length=25, default=0, null=False)
	description = models.TextField(_(u'Описание'), blank=True, default='')
	description_html = models.TextField(_(u'Описание HMTL'), editable=False)
	photo = AutoImageField(upload_to='photos', verbose_name=_(u'Фото'))
	producer = models.ForeignKey(Producer, verbose_name=_(u'Производитель'), related_name='spare_list')
	in_stock = models.BooleanField(u'В наличии')
	date_added = models.DateTimeField(_(u'Date added'), auto_now_add=True, editable=False)
	date_updated = models.DateTimeField(_(u'Date updated'), auto_now=True, editable=False)

	special_types = models.CharField(_(u'Тип специального предложения'), choices=SPECIAL_TYPES, max_length=255, blank=True)
	is_special = models.BooleanField(_(u'Выводить на главной каталога'))

	category = models.IntegerField(_(u'Категория'), max_length=50,
								choices=CATEGORIES, blank=True, null=True)
	rank = models.IntegerField(_(u'Ранжировка'), max_length=50,
								choices=RANKS, blank=True, default=0, db_column='type_')
	user_list = models.ManyToManyField(User, related_name='favorite_list', blank=True, editable=False)


	in_cart = False
	in_favorites = False
	
	class Meta:
		ordering = ['-is_special', '-date_added']
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
	address = models.TextField(_(u'Адрес'), blank=False)
	body = models.TextField(_(u'Детали'), editable=False)
	read = models.BooleanField(_(u'"прочитано"'), default=False, editable=False)
	date_added = models.DateTimeField(_(u'"добавлено"'), auto_now_add=True, editable=False)
	status = models.IntegerField(u'Статус', choices=STATUSES, max_length=255, editable=False, default=0)
	coupon = models.CharField(u'Купон', max_length=50, blank=True, default='')

	total_sum = models.IntegerField(u'Сумма', default=0, editable=False)

	user = models.ForeignKey(User, related_name='order_list', editable=False)

	class Meta:
		verbose_name = _(u'Заказ')
		verbose_name_plural = _(u'Заказы')
		ordering = ['-date_added', '-id']

	def get_readable_status(self):
		return dict(self.STATUSES)[int(self.status)]

	def get_body_html(self):
		return self.body.replace('\n', '<br>')

	def get_user(self):
		try:
			return self.user
		except DoesNotExist:
			return None

	def __unicode__(self):
		if self.date_added:
			return '%s, %s' % (
				self.date_added.strftime('%Y.%m.%d'),
				self.name
			)
		return ''

	def read_helper(self):
		return '<a href="" class="read-action" id="readAction%s">%s</a>' % (
			self.id, u'Отметить непрочитанным' if self.read else u'Отметить прочитанным')
	read_helper.short_description = u'Действия'
	read_helper.allow_tags = True


class Coupon(models.Model):
	coupon = models.CharField(_(u'Купон'), max_length=50, blank=False)
	activated = models.BooleanField(_(u'Активирован'), default=False)


class Delivery(models.Model):
	subject = models.CharField(_(u'Тема письма'), max_length=255)
	body = models.TextField(_(u'Текст письма'))
	date_added = models.DateTimeField(_(u'"добавлено"'), auto_now_add=True, editable=False)

	class Meta:
		verbose_name = _(u'Рассылка')
		verbose_name_plural = _(u'Рассылки')
		ordering = ['-date_added', '-id']

	def __unicode__(self):
		return self.subject


class SearchQuery(models.Model):
	query = models.TextField(_(u'Запрос'), max_length=255)
	count = models.IntegerField(_(u'Количество'), default=0, null=False, blank=False)

	class Meta:
		verbose_name = _(u'Поисковый запрос')
		verbose_name_plural = _(u'Поисковые запросы')
		ordering = ['-count']

	def __unicode__(self):
		return '%s, %s' % (self.query, self.count)


def format_text(text=None):
	if text is None:
		return ''
		
	text = re.sub(r'\n\n', '</p>\n\n<p>', text)
	text = re.sub(r'\n', '<br/>', text)
	
	return text