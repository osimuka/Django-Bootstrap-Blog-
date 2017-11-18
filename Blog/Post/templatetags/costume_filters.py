from django import template
from django.utils.translation import gettext
import re
import html


register = template.Library()


@register.filter(name='strip_tags')
def strip_tags(value):
    '''
    This method is used to remove all html tags on the string value to allow custom styling
    used the html.unescape() method to remove all html characters from string i.e convert to human readable format
    '''
    value = re.compile(r"<.*?>").sub("", gettext(value))
    return html.unescape(value)

