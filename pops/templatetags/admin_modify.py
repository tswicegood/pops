"""
Provides custom admin_modify for the Bootstrap theme
"""
from copy import copy

# These are unmodified from Django
from django.contrib.admin.templatetags.admin_modify import (
        prepopulated_fields_js, cell_count)

from django import template
register = template.Library()

# These are unmodified, but need to be properly registered
prepopulated_fields_js = register.inclusion_tag(
        'admin/prepopulated_fields_js.html',
        takes_context=True)(prepopulated_fields_js)
cell_count = register.filter(cell_count)


@register.inclusion_tag("admin/submit_line.html", takes_context=True)
def submit_row(context):
    from django.contrib.admin.templatetags.admin_modify import (
        submit_row as django_submit_row)
    new_context = copy(context)
    new_context.update(django_submit_row(context))
    return new_context
