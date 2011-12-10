import os
from urlparse import urljoin

from django.db                              import models
from sfModel                                import SFModel
from django.contrib.contenttypes.models     import ContentType
from django.contrib.contenttypes            import generic
from django.contrib.auth.models             import User
from SFDjangoUtils.middleware.threadlocals  import get_current_user
from settings                               import MEDIA_ROOT, MEDIA_URL

try:
    from settings import GENERIC_FILE_DIRECTORY
except:
    GENERIC_FILE_DIRECTORY = "generic_files"

from django.forms                           import ModelForm

class SFFileManager(models.Manager):

    def get_for_object(self, obj):
        """
        Create a queryset matching all files associated with the given
        object.
        """
        ctype = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=ctype.pk, object_id=obj.pk, active=True)

    def update_files(self, obj, file_list, erase_existing = True):
        """
        Update files associated with an object.
        """
        ctype = ContentType.objects.get_for_model(obj)

        if erase_existing:
            # Delete current files associated to this obj
            self.filter(content_type__pk=ctype.pk, object_id=obj.pk, active=True).delete()

        for item in file_list:
            SFFile.objects.create(content_object = obj, filename = item['filename'], file = item['file'], mime_type=item['mime_type'])

    def add_file(self, obj, filename, file, mime_type=''):
        """
        Associates the given object with a file.
        """
        self.update_files(obj, [{'filename':filename, 'file':file, 'mime_type':mime_type}], erase_existing = False)

    def remove_file(self, obj, file_id):
        ctype = ContentType.objects.get_for_model(obj)
        SFFile.objects.get(id=file_id, content_type__pk=ctype.pk, object_id=obj.pk, active=True).logicalDeletion()


class SFFile(SFModel):

    # custom file PATH
    def set_file_path(self, filePath):
        self.filePath = filePath

    def get_file_path(self, filename):
        if hasattr(self, "filePath"):
            return self.filePath
        return os.path.join(GENERIC_FILE_DIRECTORY, filename)

    filename       = models.CharField(max_length = 200, null = True, blank = True)
    file           = models.FileField(upload_to = get_file_path)
    mime_type      = models.CharField(max_length = 200, null = True, blank = True)
    content_type   = models.ForeignKey(ContentType, null=True, blank=True)
    object_id      = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    objects        = SFFileManager()

    def fieldName(self):
        return self.filename

    def permalink(self):
        permalink = ""
        filePath = self.file.path.replace(MEDIA_ROOT, "")
        permalink = urljoin(MEDIA_URL, filePath[1:])

        return permalink

    def delete(self):
        # deleting the associated file
        # trying sorl before file system
        try:
            from sorl.thumbnail import delete
            delete(self.file.file)
        except:
            os.remove(self.file.path)

        super(SFFile, self).delete()

    def __unicode__(self):
        return self.filename

    class Meta:
        app_label = "SFDjangoUtils"
        verbose_name = "SFFile"
        verbose_name_plural = "SFFiles"
        ordering  = ("created_on",)

class SFFileForm(ModelForm):

    class Meta:
        model = SFFile
        exclude = ('content_type', 'object_id', 'content_object', 'uploaded_by', 'uploaded_on', 'active')

    def set_file_path(self, filePath):
        self.filePath = filePath

    def save(self, cobj, filename, commit=True):

        if not self.is_valid():
            return None

        sffile = super( SFFileForm, self ).save(commit=False)
        sffile.content_object = cobj
        sffile.filename = filename

        if hasattr(self, "filePath"):
            sffile.set_file_path(self.filePath)

        upFile = self.cleaned_data['file']
        sffile.mime_type = upFile.content_type

        if commit:
            sffile.save()

        return sffile

