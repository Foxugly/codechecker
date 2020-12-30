from django.conf import settings
from django.db import models

from tools.generic_class import GenericClass


# Create your models here.
class Document(GenericClass):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(default="", blank=True)
    path = models.FilePathField(allow_files=True, allow_folders=True, blank=True, path=settings.MEDIA_DIR,
                                recursive=True, )
    has_default = models.BooleanField(default=False)
    extension = models.ForeignKey("language.extension", blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(GenericClass, self).save(*args, **kwargs)
