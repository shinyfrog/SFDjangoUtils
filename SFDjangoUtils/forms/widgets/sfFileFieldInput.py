from django.forms import FileInput
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext, ugettext_lazy
from django.template          import loader, Context


from SFDjangoUtils.models import SFFile

class SFFileFieldInput(FileInput):

    def render(self, name, value, attrs=None):
        inputRendered = super(SFFileFieldInput, self).render(name, value, attrs)

        if value:
            file = SFFile.objects.get(id=value)

            template = loader.get_template('SFDjangoUtils/widgets/sfFileFieldWidget.html')
            context = Context({'file':file})
            fileInputAddition = template.render(context)

            inputRendered =  fileInputAddition + inputRendered

        return mark_safe(inputRendered)

