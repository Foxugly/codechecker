from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from tools.generic_class import GenericClass


# Create your models here.
class Answer(GenericClass):
    refer_question = models.ForeignKey("question.Question", on_delete=models.CASCADE, related_name="refer_question")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    code = models.ManyToManyField("document.Document", blank=True, verbose_name=_("code"))
    path = models.FilePathField(path=settings.MEDIA_DIR, recursive=True, allow_folders=True, allow_files=False)
    language = models.ForeignKey("language.Language", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}-{1}".format(self.refer_question.slug, self.user.netid)

    def get_absolute_path(self, user):
        return self.refer_quesion.get_user_absolute_path(user)

    def get_relative_path(self, user):
        return self.refer_question.get_user_relative_path(user)

    def get_code_content(self, indice=0):
        out = ""
        if indice <= len(self.code.all()):
            with open(self.code.all()[indice].path, "r") as f:
                out = f.read()
        return out

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
