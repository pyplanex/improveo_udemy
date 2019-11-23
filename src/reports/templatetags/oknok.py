from django import template

register = template.Library()

@register.filter
def oknok(value, value2):
    try:
        if (value-value2) >= 0:
            return "OK"
        else:
            return "Not OK"
    except:
        pass