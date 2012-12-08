from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

import spares.views
import pages.views
import account.views

urlpatterns = patterns('',
	# Example:
	# (r'^lift_fit/', include('lift_fit.foo.urls')),
	
	(r'^', include('pages.urls')),

	url(r'^catalog/$', spares.views.index, name='spares-index'),
	url(r'^proizvoditel/(?P<slug>[-\w\d_]+)-(?P<id>\d+)/$', spares.views.producer_detail, name='spares-producer-detail'),
	url(r'^proizvoditel/$', spares.views.producer_detail, name='spares-producer-detail'),
	url(r'^search/$', spares.views.search, name='spares-search'),
	url(r'^(proizvoditel|producer)/(None\-)?(?P<id>\d+)/$', spares.views.producer_detail_redirect),
	url(r'^manage-cart/$', spares.views.manage_cart),
	url(r'^manage-favorites/$', spares.views.manage_favorites),
	url(r'^get-cart/$', spares.views.get_cart),
	url(r'^order/cart/$', spares.views.cart, name='order-cart'),
	url(r'^order/form/$', spares.views.order, name='order-form'),

	url(r'^account/register/$', account.views.register, name='account-register'),
	url(r'^account/logout/$', account.views.logout, name='account-logout'),
	url(r'^account/login/$', account.views.login, name='account-login'),
	url(r'^account/login-email/$', account.views.login_email, name='account-login-email'),
	url(r'^account/edit/$', account.views.edit, name='account-edit'),
	url(r'^account/favorites/$', account.views.favorites, name='account-favorites'),
	url(r'^account/restore-password/$', account.views.restore_password, name='account-restore-password'),
	url(r'^account/change-password/$', account.views.change_password, name='account-change-password'),
	url(r'^account/$', account.views.account, name='account-account'),

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
