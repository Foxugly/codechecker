from django.conf import settings
from django.db import models
import os
from tools.generic_class import GenericClass


# Create your models here.
class Document(GenericClass):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(default="", blank=True)
    path = models.FilePathField(allow_files=True, allow_folders=True, blank=True, path=settings.MEDIA_DIR,
                                recursive=True, )
    file = models.FileField(blank=True, upload_to=settings.UPLOAD_DIR)
    has_default = models.BooleanField(default=False)
    extension = models.ForeignKey("language.extension", blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    def get_download_url(self):
        return self.get_absolute_url()  # TODO
