# *-* coding: utf-8 *-*
""" Newforms Admin configuration for Photologue

"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import *

def messages_make_read(modeladmin, request, qs):
	qs.update(read=True)
messages_make_read.short_description = _(u'Отметить прочитанным')

def messages_make_unread(modeladmin, request, qs):
	qs.update(read=False)
messages_make_unread.short_description = _(u'Отметить непрочитанным')

class PageAdmin(admin.ModelAdmin):
  list_display = ('name', 'title', 'date_added')
  list_filter = ['date_added']
  #prepopulated_fields = {'slug': ('title',)}
  date_hierarchy = 'date_added'
  fieldsets = (
  	(None, {
  		'fields': ('title', 'text',)
  	}),
  	(u'Для поисковиков', {
  		'classes': ('collapse',),
  		'fields': ('page_title', 'meta_keywords', 'meta_description',),
  	}),
  )

class MessageAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'body', 'admin_files', 'read', 'read_helper')
	list_filter = ['date_added', 'read']
	actions = [messages_make_read, messages_make_unread]

class MessageFileAdmin(admin.ModelAdmin):
  list_filter = ['date_added']
  list_display = ('name', 'admin_preview', 'admin_message',)
    
admin.site.register(Page, PageAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageFile, MessageFileAdmin)