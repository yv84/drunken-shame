from django import template


register = template.Library()

@register.filter(name='field_name')
def field_name(value, arg):
    return value._meta.get_field(arg).verbose_name

@register.filter(name='field_value')
def field_value(value, arg):
    return getattr(value, arg)
