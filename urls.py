from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

import spares.views
import pages.views

urlpatterns = patterns('',
	# Example:
	# (r'^lift_fit/', include('lift_fit.foo.urls')),
	
	(r'^', include('pages.urls')),
	
	url(r'^proizvoditel/(?P<slug>[-\w\d_]+)-(?P<id>\d+)/$', spares.views.producer_detail, name='spares-producer-detail'),
	url(r'^(proizvoditel|producer)/(None\-)?(?P<id>\d+)/$', spares.views.producer_detail_redirect),

	url(r'^posts/?$', pages.views.post_list, name='pages-post-list'),
	url(r'^posts/(?P<slug>[-\w\d_]+)-(?P<id>\d+)/$', pages.views.post_detail, name='pages-post-detail'),
	
	# Uncomment the admin/doc line below to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
	url(r'^admin_tools/', include('admin_tools.urls')),

	# (r'^sentry/', include('sentry.urls')),
	
	(r'^static/(?P<path>.*)', 'django.views.static.serve',
		{ 'document_root': settings.MEDIA_ROOT }),

	url(r'^(?P<slug>.*)/$', pages.views.page, name='pages-custom-page')
)
