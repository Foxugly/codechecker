import os

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.safestring import SafeString
from django.utils.translation import gettext as _

from tools.generic_class import GenericClass


# Create your models here.
class Course(GenericClass):
    name = models.CharField(max_length=255, db_index=True)
    year = models.ForeignKey("year.Year", blank=True, on_delete=models.CASCADE)
    slug = models.SlugField()
    chapters = models.ManyToManyField("chapter.Chapter", blank=True, verbose_name=_("Chapters"))
    description = models.TextField(default="", blank=True, verbose_name=_("Description"))

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.name


    def get_relative_courses_path(self):
        return os.path.join(settings.MEDIA_DIR, settings.COURSES_DIR)

    def get_absolute_courses_path(self):
        return os.path.abspath(self.get_relative_courses_path())

    def get_user_relative_path(self, user):
        return os.path.join(settings.MEDIA_DIR, settings.STUDENTS_DIR, user.netid, self.slug)

    def get_user_absolute_path(self, user):
        return os.path.abspath(self.get_user_relative_path())

    def get_relative_path(self):
        return os.path.join(self.get_relative_courses_path(), self.slug)

    def get_absolute_path(self):
        return os.path.abspath(self.get_relative_path())


    def fullname(self):
        return "{} ({})".format(self.name, self.slug.lower())

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify("{0} - {1}".format(self.year.name, self.name))
        if not os.path.isdir(self.get_relative_path()):
            if not os.path.isdir(settings.MEDIA_DIR):
                os.mkdir(settings.MEDIA_DIR, settings.RIGHTS_DIR)
            if not os.path.isdir(self.get_relative_courses_path()):
                os.mkdir(self.get_relative_courses_path(), settings.RIGHTS_DIR)
            os.mkdir(self.get_relative_path(), settings.RIGHTS_DIR)
        super(GenericClass, self).save(*args, **kwargs)

    def get_json(self):
        return SafeString([c.get_json() for c in self.chapters.all()])
