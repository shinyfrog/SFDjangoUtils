from django.contrib.auth.models import User
from django.db                  import models
from SFDjangoUtils.middleware   import threadlocals

from SFDjangoUtils.middleware.threadlocals import get_current_user

class SFActiveModelManager(models.Manager):
    def get_query_set(self):
        return super(SFActiveModelManager, self).get_query_set().filter(active=True)


class SFActiveNotDraftModelManager(models.Manager):
    def get_query_set(self):
        return super(SFActiveNotDraftModelManager, self).get_query_set().filter(active=True, draft=False)


class SFModelManager(models.Manager):
    def get_query_set(self):
        return super(SFModelManager, self).get_query_set()


class SFModel(models.Model):
    created_by = models.ForeignKey(User, related_name = "%(app_label)s_%(class)s_created_by", blank = True, null = True, editable = True)
    updated_by = models.ForeignKey(User, related_name = "%(app_label)s_%(class)s_updated_by", blank = True, null = True, editable = True)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    active     = models.BooleanField(default = True)
    draft      = models.BooleanField(default = True)
    annotation = models.TextField(blank = True, null = True)

    objects = SFModelManager()
    active_objects = SFActiveModelManager()
    active_not_draft_object = SFActiveNotDraftModelManager()
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        u = get_current_user()

        if u is not None and u.is_authenticated():
            self.updated_by = u
            # If the object does not exist, it hasn't an id
            if not self.id:
                self.created_by = self.updated_by

        super(SFModel, self).save(*args, **kwargs)

    def logicalDeletion(self):
        self.active = False
        self.save()

    # SFFile 
    def _get_files(self):
        from sfFile import SFFile
        if not self.id: return []
        return SFFile.objects.get_for_object(self)

    def _set_files(self, file_list, erase_existing = True):
        from sfFile import SFFile
        if not self.id:
            raise Exception("This object has not an id. You MUST call the 'save' method before do this.")
        SFFile.objects.update_files(self, file_list)

    files = property(_get_files, _set_files)

    def addFile(self, filename, file):
        from sfFile import SFFile
        SFFile.objects.add_file(self, filename, file)
