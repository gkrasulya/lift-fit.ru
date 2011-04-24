from django import template

from spares.models import *

register = template.Library()

class ProducerListNode(template.Node):
	def __init__(self, varname):
		self.varname = varname
		
	def render(self, context):
		context[self.varname] = Producer.objects.all()
		return ''

class RandomSpareListNode(template.Node):
	def __init__(self, varname):
		self.varname = varname

	def render(self, context):
		context[self.varname] = Spare.objects.order_by('?')[:2]
		return ''
		
@register.tag
def get_producer_list(parser, token):
	"""return producer list for representing in main menu"""
	contents = token.split_contents()
	if len(contents) != 3:
		raise template.TemplateSyntaxError, '%r tag takes exactly 2 arguments' % contents[0]
	if contents[1] != 'as':
		raise template.TemplateSyntaxError, '%r tag: second argument must be "as"' % contents[0]
		
	return ProducerListNode(contents[2])

@register.tag
def get_random_spare_list(parser, token):
	contents = token.split_contents()
	if len(contents) != 3:
		raise template.TemplateSyntaxError, '%r tag takes exactly 2 arguments' % contents[0]
	if contents[1] != 'as':
		raise template.TemplateSyntaxError, '%r tag: second argument must be "as"' % contents[0]

	return RandomSpareListNode(contents[2])
