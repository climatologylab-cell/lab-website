from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    """
    Returns the value turned into a list.
    """
    if value:
        return value.split(key)
    return []

@register.filter(name='trim')
def trim(value):
    """
    Returns the value stripped of leading and trailing whitespace.
    """
    if value:
        return value.strip()
    return ""
