from django import template

register = template.Library()

@register.filter
def substract(value, value2):
    try:
        return value-value2
    except:
        pass