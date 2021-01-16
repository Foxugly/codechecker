from django.conf import settings
from django.db import models
from tools.generic_class import GenericClass
from django.urls import reverse
import inspect


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

    def get_delete_popup_url(self):
        return reverse("document:document_ajax_delete", kwargs={'document_id': self.id})

    def get_buttons(self, buttons):
        out = ''
        if "detail" in buttons:
            out += '<a class="btn btn-sm btn-primary ml-1" href="{0}"><i class="far fa-eye"></i></a>'.format(
                self.get_absolute_url())
        if "change" in buttons:
            out += '<a class="btn btn-sm btn-info ml-1" href="{0}"><i class="fas fa-edit"></i></a>'.format(
                self.get_change_url())
        if "download" in buttons:
            out += '<a class="btn btn-sm btn-success ml-1" href="{0}"><i class="fas fa-download"></i></a>'.format(
                self.get_download_url())
        if "delete" in buttons:
            out += '<a class="btn btn-sm btn-danger confirmation ml-1" data-url="{0}" href="#" data-name="{1}"><i class="far fa-trash-alt"></i></a>'.format(self.get_delete_popup_url(), self.name)
        return out
