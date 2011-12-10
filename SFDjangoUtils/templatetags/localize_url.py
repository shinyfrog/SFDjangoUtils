import os.path
from django.utils.safestring        import mark_safe
from django                         import template
from django.template.defaultfilters import stringfilter
from settings                       import AVAILABLE_LANGUAGES

register = template.Library()

@register.filter
@stringfilter
def localize_url(page_path, language):

    language_urls = ["/" + k + "/" for k,v in AVAILABLE_LANGUAGES.items()]

    if page_path[:4] in language_urls:
        page_path = "/" + language + "/" + page_path[4:]
    else:
        page_path = "/" + language + page_path

    return mark_safe(page_path)

