import jinja2
import markdown as markdown_package
from coffin import template

register = template.Library()

__author__ = 'mikhailturilin'

@register.filter()
def markdown(html):
    '''
    Markdown filter
    Usage:
        {% filter markdown %}
        html code
        {% endfilter %}
    '''
    lines = [line.strip() for line in html.splitlines()]
    html = "\n".join(lines)

    return jinja2.Markup(markdown_package.markdown(html))