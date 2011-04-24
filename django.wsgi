# -*- encoding: utf-8 -*- 

import os, sys
sys.path.insert(0, os.path.join(os.path.expanduser('~'), 'django-1.3'))
sys.path.insert(0, os.path.join(os.path.expanduser('~'), 'django-projects/lift_fit'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()