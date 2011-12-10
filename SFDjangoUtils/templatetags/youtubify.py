'''
Youtubify replaces all YouTube links with the player
'''
__version__ = "0.1"
__author__ = "Konstantin V. Erokhin"
__contact__ = "http://www.shinyfrog.net"
__date__ = 'Tue Jul 26 11:26:53 2011'
__timestamp__ = '1311672413'

import re
from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()
youtube_pat = re.compile(r'(https?://)?(www\.)?youtube\.([\w-]+)/watch\?v=([-\w]+)(&[-\w]+=*([-\w]+)*)*')
youtube_short_pat = re.compile(r'(https?://)?(www\.)?youtu\.be/([-\w]+)[/?]*(&*[-\w]+=*([-\w]+)*)*')
width = 0
height = 0

def get_script(m):
    link = m.group()
    if '?v=' in link:
        video_code = link.split('?v=')[1].split('&')[0].split('?')[0].split('/')[0]
    else:
        video_code = link.split('youtu.be/')[1].split('&')[0].split('?')[0].split('/')[0]


    return '<iframe width="' + width + '" height="' + height + '" src="http://www.youtube.com/embed/' + video_code + '?modestbranding=1&showinfo=0&rel=0" class="youTubePlayer" frameborder="0" allowfullscreen></iframe>'
    
@register.filter
@stringfilter
def youtubify(text, dimensions):
    if dimensions is None:
        return False

    global width, height
    dimensions_list = [dimensions.strip() for dimensions in dimensions.split('x')]
    width = dimensions_list[0]
    height = dimensions_list[1]

    # De-encoding HTML &
    text = text.replace('&amp;', '&')
    # lowing "youtu.be" for token finding
    pattern = re.compile('youtu.be', re.IGNORECASE)
    text = pattern.sub('youtu.be', text)

    text = youtube_pat.sub(get_script, text)
    text = youtube_short_pat.sub(get_script, text)
    return mark_safe(text)
