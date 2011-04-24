from django import template
from django.contrib.admin.templatetags.admin_list import result_list

register = template.Library()

#result_message_list = register.inclusion_tag("admin/pages/message/change_list_results.html")(result_list)