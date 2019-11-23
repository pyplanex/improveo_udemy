from django import template
register = template.Library()


@register.filter
def pic_name(path):
    name = path.split('/')[-1]
    return name
