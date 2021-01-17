from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from tools.generic_class import GenericClass


# Create your models here.
class Answer(GenericClass):
    refer_question = models.ForeignKey("question.Question", on_delete=models.CASCADE, related_name="refer_question")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    docs = models.ManyToManyField("document.Document", blank=True, verbose_name=_("documents"), related_name="docs")
    codes = models.ManyToManyField("document.Document", blank=True, verbose_name=_("codes"), related_name="codes")
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
        if len(self.codes.all()):
            if indice <= len(self.codes.all()):
                with open(self.code.all()[indice].path, "r") as f:
                    out = f.read()
        return out

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')

    def get_buttons(self, buttons):
        out = ''
        if "detail" in buttons:
            out += '<a class="btn btn-sm btn-primary  ml-1" href="{0}"><i class="far fa-eye"></i></a>'.format(
                self.get_absolute_url())
        if "change" in buttons:
            out += '<a class="btn btn-sm btn-info ml-1" href="{0}"><i class="fas fa-edit"></i></a>'.format(
                self.get_change_url())
        if "delete" in buttons:
            out += '<button class="btn btn-sm btn-danger confirmation ml-1" data-url="{0}" data-name="{1}"><i class="far fa-trash-alt"></i></button>'.format(self.get_delete_popup_url(), str(self))
        return out
