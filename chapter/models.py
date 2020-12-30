import os

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _

from tools.generic_class import GenericClass


# Create your models here.
class Chapter(GenericClass):
    refer_course = models.ForeignKey("course.Course", blank=True, verbose_name=_("course"), on_delete=models.CASCADE)
    name = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    questions = models.ManyToManyField("question.Question", blank=True, verbose_name=_("questions"))

    def __str__(self):
        return self.name

    def get_relative_path(self):
        return os.path.join(self.refer_course.get_relative_path(), self.slug)

    def get_absolute_path(self):
        return os.path.join(self.refer_course.get_absolute_path(), self.slug)   

    def get_user_relative_path(self, user):
        return os.path.join(self.refer_course.get_user_relative_path(user), self.slug)

    def get_user_absolute_path(self, user):
        return os.path.join(self.refer_course.get_user_absolute_path(user), self.slug)

    class Meta:
        verbose_name = _('Chapter')
        verbose_name_plural = _('Chapters')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not os.path.isdir(self.get_relative_path()):
            os.mkdir(self.get_relative_path(), settings.RIGHTS_DIR)
        super(GenericClass, self).save(*args, **kwargs)

    def get_json(self):
        out = dict(text=self.name, href=self.get_detail_url())
        if len(self.questions.all()):
            out['nodes'] = [q.get_json() for q in self.questions.all()]
        return out
