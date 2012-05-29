"""
Provides custom admin_modify for the Bootstrap theme
"""
from copy import copy
from django.conf import settings

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

BUTTONS = {
    "save": {
        "key": "_save",
        "text": "Save",
    },
    "save_and_continue": {
        "key": "_continue",
        "text": "Save and continue editing",
    },
    "save_and_add_another": {
        "key": "_addanother",
        "text": "Save and add another",
    },
    "save_as_new": {
        "key": "_saveasnew",
        "text": "Save as new",
    },
}


@register.inclusion_tag("admin/submit_line.html", takes_context=True)
def submit_row(context):
    from django.contrib.admin.templatetags.admin_modify import (
        submit_row as django_submit_row)
    new_context = copy(context)
    new_context.update(django_submit_row(context))

    # TODO: test this
    buttons = {"primary_button": {}, "secondary_buttons": [], }
    if not getattr(settings, "POPS_SUBMIT_BUTTONS", False):
        if new_context["show_save_and_continue"]:
            buttons["primary_button"] = BUTTONS["save_and_continue"]
        else:
            buttons["primary_button"] = BUTTONS["save"]
        if new_context["show_save_and_add_another"]:
            buttons["secondary_buttons"].append(BUTTONS["save_and_add_another"])
        if new_context["show_save_as_new"]:
            buttons["secondary_buttons"].append(BUTTONS["save_as_new"])
        if new_context["show_save_and_continue"]:
            buttons["secondary_buttons"].append(BUTTONS["save"])
    else:
        configured_buttons = settings.POPS_SUBMIT_BUTTONS
        if type(configured_buttons) is list:
            buttons["primary_button"] = BUTTONS[configured_buttons[0]]
            buttons["secondary_buttons"] = [
                    BUTTONS[a] for a in configured_buttons[1:]
                    if new_context["show_%s" % a]]
        else:
            buttons = configured_buttons
    new_context["buttons"] = buttons
    return new_context
