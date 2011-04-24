from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

import spares.views

urlpatterns = patterns('',
	# Example:
	# (r'^lift_fit/', include('lift_fit.foo.urls')),
	
	(r'^', include('pages.urls')),
	
	url(r'^producer/(?P<producer_id>\d+)/$', spares.views.producer_detail, name='spares-producer-detail'),
	
	# Uncomment the admin/doc line below to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
	url(r'^admin_tools/', include('admin_tools.urls')),

	(r'^sentry/', include('sentry.urls')),
	
	(r'^static/(?P<path>.*)', 'django.views.static.serve',
		{ 'docum1ent_root': settings.MEDIA_ROOT }),
)
