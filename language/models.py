from django.db import models
from django.utils.translation import gettext as _

from tools.generic_class import GenericClass


# Create your models here.

class Extension(GenericClass):
    name = models.CharField(_("name"), max_length=16)
    mode = models.CharField(_("mode"), max_length=16)
    default_comment = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Extension')
        verbose_name_plural = _('Extensions')


class Language(GenericClass):
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    name = models.CharField(_("name"), max_length=16)
    accepted_extensions = models.ManyToManyField(Extension, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Language')
