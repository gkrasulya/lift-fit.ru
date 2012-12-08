# encoding: utf-8

from django.contrib import admin
from models import *
from forms import DeliveryForm

class ProducerAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
    	(None, {
    		'fields': ('title', 'slug', 'text', 'split_into_categories',)
    	}),
    	(u'Для поисковиков', {
    		'classes': ('collapse',),
    		'fields': ('page_title', 'meta_keywords', 'meta_description'),
    	}),
    )

class SpareAdmin(admin.ModelAdmin):
    list_display = ('admin_photo', 'title', 'producer')
    list_filter = ('producer',)

class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('query', 'count',)

class OrderAdmin(admin.ModelAdmin):
    # list_display = ('admin_photo', 'title', 'producer')
    # list_filter = ('producer',)
    pass

class DeliveryAdmin(admin.ModelAdmin):
    form = DeliveryForm
    
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Spare, SpareAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(SearchQuery, SearchQueryAdmin)
admin.site.register(Delivery, DeliveryAdmin)