# *-* coding: utf-8 *-*
from django.utils.translation import ugettext_lazy as _

from admin_tools.dashboard import modules
from models import *

class PagesInfoModule(modules.DashboardModule):
	title = _(u'Инофрмация')
	title_url = 'http://google.com'
	template = 'admin_tools/info.html'

	def is_empty(self):
		return False

	def init_with_context(self, context, **kwargs):

		super(PagesInfoModule, self).__init__(**kwargs)

		context['messages_count'] = Message.objects.count()
		context['new_messages_count'] = Message.objects.filter(read=False).count()
