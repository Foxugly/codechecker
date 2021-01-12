import os

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _

from answer.models import Answer
from document.models import Document
from language.models import Language
from tools.generic_class import GenericClass
from tinymce.models import HTMLField


# Create your models here.
class Question(GenericClass):
    refer_chapter = models.ForeignKey("chapter.Chapter", on_delete=models.CASCADE, verbose_name=_("chapter"))
    slug = models.SlugField()
    name = models.CharField(_("Title"), max_length=255)
    question = HTMLField(_("Question"), default="")
    documents = models.ManyToManyField(Document, blank=True, verbose_name=_("documents"), related_name='documents',)
    default_code = models.ManyToManyField(Document, blank=True, verbose_name=_("default_code"),
                                          related_name='default_code')
    answers = models.ManyToManyField(Answer, blank=True, verbose_name=_("answers"))
    languages = models.ManyToManyField(Language, blank=True)
    can_add_documents = models.BooleanField(default=False)
    can_add_code = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not os.path.isdir(self.get_relative_path()):
            os.mkdir(self.get_relative_path(), settings.RIGHTS_DIR)
        super(GenericClass, self).save(*args, **kwargs)
        if self.refer_chapter:
            if self not in self.refer_chapter.questions.all():
                self.refer_chapter.questions.add(self)

    def init_default_code(self):
        if not self.default_code.exists() and self.languages.exists():
            lang = self.languages.all()[0]
            ext = lang.accepted_extensions.all()[0]
            default = "code.{}".format(ext.name)
            path_question = os.path.join(self.get_relative_path(), default)
            with open(path_question, "w") as f:
                f.write(ext.default_comment)
                doc = Document(name=default, path=path_question, extension=ext)
                doc.save()
            self.default_code.add(doc)

    def get_absolute_path(self):
        return os.path.join(self.refer_chapter.get_absolute_path(), self.slug)

    def get_relative_path(self):
        return os.path.join(self.refer_chapter.get_relative_path(), self.slug)

    def get_user_absolute_path(self, user):
        return os.path.join(self.refer_chapter.get_user_absolute_path(user), self.slug)

    def get_user_relative_path(self, user):
        return os.path.join(self.refer_chapter.get_user_relative_path(user), self.slug)

    def get_json(self):
        return dict(text=self.name, href=self.get_absolute_url())
