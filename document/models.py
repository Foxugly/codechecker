from django.conf import settings
from django.db import models
from django.urls import reverse

from tools.generic_class import GenericClass


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
            out += '<a class="btn btn-sm btn-danger btn-delete confirmation ml-1" data-source="table" data-url="{0}" href="#" data-name="{1}"><i class="far fa-trash-alt"></i></a>'.format(
                self.get_delete_popup_url(), self.name)
        return out

    def get_button_download_delete(self):
        out = '<a class="ml-3" href="{0}">{1}</a>'.format(self.get_download_url(), self.name)
        out += '<a class ="ml-1 btn btn-outline-danger btn-sm btn-delete confirmation" href="#" data-source="span" data-url="{0}" data-name="{1}"><i class="fa fa-times"></i></a>'.format(
            self.get_delete_popup_url(), self.name)
        return out