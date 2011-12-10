'''
Vimeify replaces all Vimeo links with the embedded player
'''
__version__ = "0.1"
__author__ = "Konstantin V. Erokhin"
__contact__ = "http://www.shinyfrog.net"
__date__ = 'Tue Jul 26 11:37:13 2011'
__timestamp__ = '1311673033'

import re
from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()
vimeo_pat = re.compile(r'(https?://)?(www\.)?(player\.)?vimeo\.([\w-]+)/(video/)?([-\w]+)[?]*(&*[-\w]+=*([-\w]+)*)*')
width = 0
height = 0

def get_script(m):
    link = m.group()
    video_code = link.split('/')[-1].split('?')[0].split('&')[0]

    return '<iframe src="http://player.vimeo.com/video/' + video_code + '?title=0&byline=0&portrait=0&color=ffffff" width="' + width + '" height="' + height + '" class="vimeoPlayer" frameborder="0"></iframe>'
    

@register.filter
@stringfilter
def vimeify(text, dimensions):
    if dimensions is None:
        return False

    global width, height
    dimensions_list = [dimensions.strip() for dimensions in dimensions.split('x')]
    width = dimensions_list[0]
    height = dimensions_list[1]

    # De-encoding HTML &
    text = text.replace('&amp;', '&')

    text = vimeo_pat.sub(get_script, text)

    return mark_safe(text)
