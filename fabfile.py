from fabric.api import *

def rs(port='1234'):
	local('python manage.py runserver :%s' % port)