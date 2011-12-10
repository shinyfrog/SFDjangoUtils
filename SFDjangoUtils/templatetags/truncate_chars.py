'''
    encode_email adds obfuctated link for each email address found in 
    the string the filter is applied to
'''

__version__ = "0.1"
__author__ = "Konstantin V. Erokhin"
__contact__ = "http://www.shinyfrog.net"
__date__ = 'Mon Mar 14 12:01:43 2011'

from django import template

register = template.Library()

# truncate after a certain number of characters - 3 (reserved for dots)
@register.filter
def truncate_chars(value, max_chars):
    if len(value) <= max_chars:
        return value
    else:
        return value[:max_chars - 3] + '...'

