# No reason to be lazy in evaluation of translation since we
# need them all up front.
from django.utils.translation import ugettext as _

# List of phrases found in ``help_text`` on fields that don't make
# sense in the context of the Bootstrap admin.
UNHELPFUL = [
    u"%s" % _(' Hold down "Control", or "Command" on a Mac,'
            ' to select more than one.'),
]


class RemoveUnhelpfulHelpText(object):
    """
    Removes ``help_text`` that matches anything found in ``UNHELPFUL``

    This needs to be mixed in to any forms that you want to make more
    Bootstrap friendly.  It should be the first thing mixed in to ensure
    that it's run.
    """

    def __init__(self, *args, **kwargs):
        super(RemoveUnhelpfulHelpText, self).__init__(*args, **kwargs)
        self.remove_unhelpful_help_text()

    def remove_unhelpful_help_text(self):
        for name, field in self.fields.iteritems():
            for remove_text in UNHELPFUL:
                self.fields[name].help_text = u"%s" % unicode(
                    field.help_text).replace(remove_text, '')
