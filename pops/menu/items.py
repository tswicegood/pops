from admin_tools.menu import items
from django.utils.translation import ugettext_lazy as _


class SearchBox(items.MenuItem):
    """
    Add a
    """
    template = "admin_tools/menu/search.html"

    def __init__(self, app_list, placeholder=""):
        self.placeholder = placeholder
        self.app_list = app_list
        self.children = []

    def init_with_context(self, context):
        context.update({
            "placeholder": self.placeholder,
        })


class SearchableAppList(items.AppList):
    """
    Like the built-in admin-tools AppList + a search box to filter
    """

    def __init__(self, title=None, placeholder=None, **kwargs):
        if placeholder is None:
            placeholder = _("Search apps...")
        self.placeholder = placeholder
        super(SearchableAppList, self).__init__(title=title, **kwargs)

    def init_with_context(self, context):
        super(SearchableAppList, self).init_with_context(context)
        self.children.insert(0, SearchBox(self, placeholder=self.placeholder))
