from django import template
import temps.services as service

register = template.Library()


@register.inclusion_tag('temps/new_batch')
def get_current_temp():
	ct = service.get_current_temp()
	context = {'ct' : ct}
	return render(context)