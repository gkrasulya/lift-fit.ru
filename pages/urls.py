from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import views

urlpatterns = patterns('',
  url(r'^admin/pages/message/read-action/(?P<message_id>\d+)/$', views.read_action),

  url(r'^$', views.page, { 'slug': 'index' }, name='pages-index'),
  url(r'^about/$', views.page, { 'slug': 'about' }, name='pages-about'),
  
  url(r'^feedback/$', views.feedback, name='pages-feedback'),
	url(r'^feedback/thanks/$', views.feedback_thanks, name='pages-feedback-thanks'),

  url(r'^site-map/$', views.site_map, name='pages-site-map'),
  url(r'^sitemap.xml/?$', views.site_map_xml, name='pages-site-map-xml'),
  url(r'^robots.txt/?$', views.robots_txt, name='pages-robots-txt'),
)
