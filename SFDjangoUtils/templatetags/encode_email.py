'''
    encode_email adds obfuctated link for each email address found in 
    the string the filter is applied to
'''

import random
import re
import time
from django.utils.safestring        import mark_safe
from django                         import template
from django.template.defaultfilters import stringfilter
from random                         import randint

register = template.Library()
email_pat = re.compile(r'\b[-.\w]+@[-.\w]+\.[a-z]{2,4}\b')
override_label = ""

def get_script(m, display_label = ""):

    email = m.group()
    username, at, domain = email.partition("@")
    digitless_username = ''.join([letter for letter in username if not letter.isdigit()]) 
    id = digitless_username + "_" + str(randint(10000, 99999))
    reverse_email = username[::-1] + " AT " + domain[::-1] + " LAB " + override_label[::-1]
    end_line = ""

    return "<a id=\"" + id + "\" href=\"#\">" + end_line \
            + reverse_email + end_line \
            + "</a>" + end_line \
            + "<script type=\"text/JavaScript\">" + end_line \
            + "var e=document.getElementById(\"" + id + "\");" + end_line \
            + "var d=/ AT /;" + end_line \
            + "var i=/ LAB /;" + end_line \
            + "var h=document.createElement(\"a\");" + end_line \
            + "h.innerHTML=e.innerHTML.split(i)[0];" + end_line \
            + "h.id=\"" + id + "_m\";" + end_line \
            + "if (e.innerHTML.split(d)[1].split(i)[1]!=\"\" && e.innerHTML.split(d)[1].split(i)[1]!=undefined){" + end_line \
            + "e.innerHTML=e.innerHTML.split(d)[1].split(i)[1];" + end_line \
            + "}else{" + end_line \
            + "e.innerHTML=e.innerHTML.split(d)[1].split(i)[0]+\"@\"+e.innerHTML.split(d)[0];" + end_line \
            + "};" + end_line \
            + "h.style.display=\"none\";" + end_line \
            + "e.appendChild(h);" + end_line \
            + "e.onclick=function(){" + end_line \
            + "location.href=\"mailto:\"+(document.getElementById(\"" + id + "_m\").innerHTML.split(d)[1]+\"@\"+document.getElementById(\"" + id + "_m\").innerHTML.split(d)[0]).split(\"\").reverse().join(\"\");" + end_line \
            + "};" + end_line \
            + "e.style.unicodeBidi=\"bidi-override\";" + end_line \
            + "e.style.direction=\"rtl\";" + end_line \
            + "e.style.whiteSpace=\"nowrap\";" + end_line \
            + "</script>"

@register.filter
@stringfilter
def encode_email(text, label = ""):
    global override_label
    override_label = label
    text = email_pat.sub(get_script, text)
    return mark_safe(text)
