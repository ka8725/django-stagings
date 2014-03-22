from django import template
from django.template import defaultfilters as filters

register = template.Library()

@register.filter
def author_link(author):
  return filters.safe("""
    <a href='http://google.com?q={author}' target='_blank'>
      {author}
    </a>""".format(author=author))
