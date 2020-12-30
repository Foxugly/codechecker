from django.db import models
from django.utils.translation import gettext as _

from tools.generic_class import GenericClass


# Create your models here.
class Year(GenericClass):
    name = models.CharField(_("name"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Year')
        verbose_name_plural = _('Years')
