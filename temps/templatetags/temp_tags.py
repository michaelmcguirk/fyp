from django import template
import temps.services as service

register = template.Library()


@register.assignment_tag
def get_current_temp():
	ct = service.get_current_temp()
	return {'ct' : ct}