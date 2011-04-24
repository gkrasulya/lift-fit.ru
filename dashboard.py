# *-* coding: utf-8 *-*

"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'lift_fit.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'lift_fit.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.menu import items, Menu
from admin_tools.utils import get_admin_site_name

from pages.admin_modules import *


class CustomMenu(Menu):
    def __init__(self, **kwargs):
        super(CustomMenu, self).__init__(**kwargs)
        self.children = (
            items.MenuItem(_(u'Главная панель'), '/admin/'),
            items.ModelList(_(u'Applications'),
                models=('pages.models.*', 'spares.models.*', )),
            items.ModelList(_(u'Administration'),
                models=('django.contrib.auth.models.*',)),
        )


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for lift_fit.
    """
    columns = 2

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_(u'Статистика посещений'),
                 'http://metrika.yandex.ru/stat/?id=5566567'],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

        self.children.append(PagesInfoModule(
            title_url='',
            content='asdasdasds',
        ))

        self.children.append(modules.ModelList(
            deletable=False,
            collapsible=False,
            title=_(u'Applications'),
            models=('pages.models.*', 'spares.models.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for lift_fit.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models)
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)