from django import template
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site

from BeautifulSoup import BeautifulSoup

from ..conf import settings


register = template.Library()


@register.simple_tag
def site_link():
    # TODO: Convert this to a template-based tag
    if settings.POPS_SITE_LINK:
        return '''
            <li class="visible-desktop">
                <a href="%s"  class="top-icon" title="%s" rel="popover"
                        data-placement="below">
                    <i class="icon-home icon-white"></i>
                </a>
            </li>
            <li class="divider-vertical visible-desktop"></li>
            ''' % (settings.POPS_SITE_LINK, _('Open site'))
    else:
        return ''


@register.simple_tag
def site_name():
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        return Site.objects.get_current().name
    else:
        return _('Django site')


# breadcrumbs tag
class BreadcrumbsNode(template.Node):
    """
        renders bootstrap breadcrumbs list.
        usage::
            {% breadcrumbs %}
            url1|text1
            url2|text2
            text3
            {% endbreadcrumbs %}
        | is delimiter by default, you can use {% breadcrumbs delimiter_char %}
        to change it.

        lines without delimiters are interpreted as active breadcrumbs

    """
    def __init__(self, nodelist, delimiter):
        self.nodelist = nodelist
        self.delimiter = delimiter

    def render(self, context):
        # TODO: convert this to a template-based tag
        data = self.nodelist.render(context).strip()

        if not data:
            return ''

        try:
            data.index('<div class="breadcrumbs">')
        except ValueError:
            lines = [l.strip().split(self.delimiter) for l in data.split("\n")
                    if l.strip()]
        else:
            # data is django-style breadcrumbs, parsing
            try:
                soup = BeautifulSoup(data)
                lines = [(a.get('href'), a.text) for a in soup.findAll('a')]
                lines.append(
                        [soup.find('div').text.split('&rsaquo;')[-1].strip()])
            except Exception, e:
                lines = [["Cannot parse breadcrumbs: %s" % unicode(e)]]

        out = '<ul class="breadcrumb">'
        curr = 0
        for d in lines:
            if d[0][0] == '*':
                active = ' class="active"'
                d[0] = d[0][1:]
            else:
                active = ''

            curr += 1
            if (len(lines) == curr):
                # last
                divider = ''
            else:
                divider = '<span class="divider">/</span>'

            if len(d) == 2:
                out += '<li%s><a href="%s">%s</a>%s</li>' % (
                        active, d[0], d[1], divider)
            elif len(d) == 1:
                out += '<li%s>%s%s</li>' % (active, d[0], divider)
            else:
                raise ValueError(
                        'Invalid breadcrumb line: %s' % self.delimiter.join(d))
        out += '</ul>'
        return out


@register.tag(name='breadcrumbs')
def do_breadcrumbs(parser, token):
    try:
        tag_name, delimiter = token.contents.split(None, 1)
    except ValueError:
        delimiter = '|'

    nodelist = parser.parse(('endbreadcrumbs',))
    parser.delete_first_token()

    return BreadcrumbsNode(nodelist, delimiter)
