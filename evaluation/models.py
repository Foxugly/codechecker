from django.db import models
from django.utils.translation import gettext as _
from users.models import User
from tools.generic_class import GenericClass
from django.urls import reverse
from django.core.exceptions import ValidationError
# Create your models here.


class Criteria(GenericClass):
    STEPS_CHOICES = (
        (0.25, "0,25"),
        (0.5, "0,5"),
        (1, "1"),
    )

    refer_question = models.ForeignKey("question.Question", verbose_name="refer_question", blank=True, on_delete=models.CASCADE)
    name = models.CharField(_("Criteria"), max_length=255)
    detail = models.TextField(blank=True, null=True)
    max_points = models.DecimalField(default=4, decimal_places=2, max_digits=4)
    step = models.DecimalField(_("Step"), default=1, decimal_places=2, max_digits=4, choices=STEPS_CHOICES)

    def save(self, *args, **kwargs):
        super(GenericClass, self).save(*args, **kwargs)
        if self.refer_question:
            if self not in self.refer_question.criterias.all():
                self.refer_question.criterias.add(self)

    def get_buttons(self, buttons):
        out = ''
        if "detail" in buttons:
            out += '<a class="btn btn-sm btn-primary btn-modal ml-1" href="{0}"><i class="far fa-eye"></i></a>'.format(
                self.get_absolute_url())
        if "change" in buttons:
            out += '<a class="btn btn-sm btn-info btn-modal ml-1" href="#" data-url="{0}"><i class="fas fa-edit"></i></a>'.format(
                self.get_change_url())
        if "download" in buttons:
            out += '<a class="btn btn-sm btn-success ml-1" href="{0}"><i class="fas fa-download"></i></a>'.format(
                self.get_download_url())
        if "delete" in buttons:
            out += '<a class="btn btn-sm btn-danger btn-delete confirmation ml-1" data-source="table" data-url="{0}" href="#" data-name="{1}"><i class="far fa-trash-alt"></i></a>'.format(
                self.get_delete_popup_url(), self.name)
        return out

    def get_absolute_url(self):
        return reverse("evaluation:criteria_detail", kwargs={'pk': self.pk})

    def get_change_url(self):
        return reverse("evaluation:criteria_change", kwargs={'pk': self.pk})

    def get_detail_url(self):
        return self.get_absolute_url()

    def get_downlad_url(self):
        return self.get_absolute_url()

    def get_delete_url(self):
        return reverse("evaluation:criteria_delete", kwargs={'pk': self.pk})

    def get_delete_popup_url(self):
        return reverse("evaluation:criteria_ajax_delete", kwargs={'criteria_id': self.id})


class Evaluation(GenericClass):
    refer_criteria = models.ForeignKey(Criteria, blank=True, on_delete=models.CASCADE)
    refer_user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    points = models.DecimalField(default=0,  decimal_places=2, max_digits=4)
    explanation = models.TextField(blank=True, null=True)
