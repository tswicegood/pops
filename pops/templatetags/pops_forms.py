from django import template
from django.utils.safestring import mark_safe
register = template.Library()

SIMPLE_INPUT = """
<input type="%(type)s" id="id_%(name)s" name="%(name)s" value="%(value)s">
""".strip()


@register.filter
def as_hidden_field(field):
    """Return a field as a simple hidden field"""
    value = field.value()
    if value is None:
        value = ""
    return mark_safe(SIMPLE_INPUT % {
        "type": "hidden",
        "name": field.name,
        "value": value,
    })
