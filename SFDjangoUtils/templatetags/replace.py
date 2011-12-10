'''
    http://djangosnippets.org/snippets/60/
    This will perform a regular expression search/replace on a string in your template.
    {% load replace %} {{ mystring|replace:"/l(u+)pin/m\1gen" }}
    If: mystring = 'lupin, luuuuuupin, and luuuuuuuuuuuuupin are le pwn' then it will return: mugen, muuuuuugen, and muuuuuuuuuuuuugen are le pwn
    The argument is in the following format:
    [delim char]regexp search[delim char]regexp replace
'''
__version__ = "0.1"
__author__ = "Konstantin V. Erokhin"
__contact__ = "http://www.shinyfrog.net"
__date__ = 'Wed May 25 17:53:49 2011'
__timestamp__ = '1306338829'

import re 

from django import template
register = template.Library()

@register.filter
def replace ( string, args ): 
    search  = args.split(args[0])[1]
    replace = args.split(args[0])[2]

    return re.sub( search, replace, string )

