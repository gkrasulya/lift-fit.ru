# encoding: utf-8

from django.contrib import admin
from models import *

class ProducerAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fieldsets = (
    	(None, {
    		'fields': ('title',)
    	}),
    	(u'Для поисковиков', {
    		'classes': ('collapse',),
    		'fields': ('page_title', 'meta_keywords', 'meta_description'),
    	}),
    )

class SpareAdmin(admin.ModelAdmin):
    list_display = ('admin_photo', 'title', 'producer')
    list_filter = ('producer',)
    
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Spare, SpareAdmin)