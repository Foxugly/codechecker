import os
import subprocess

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _

from answer.models import Answer
from document.models import Document
from language.models import Language
from tools.generic_class import GenericClass
from tinymce.models import HTMLField
from evaluation.models import Criteria, Evaluation


class Question(GenericClass):
    doc_buttons = ['add', 'detail', 'download', 'delete']
    code_buttons = ['add', 'detail', 'download', 'delete']
    answers_buttons = ['detail']
    criterias_buttons = ['change', 'delete']
    refer_chapter = models.ForeignKey("chapter.Chapter", on_delete=models.CASCADE, verbose_name=_("chapter"))
    slug = models.SlugField()
    name = models.CharField(_("Title"), max_length=255)
    question = HTMLField(_("Question"), default="")
    documents = models.ManyToManyField(Document, blank=True, verbose_name=_("documents"), related_name='documents',)
    default_code = models.ManyToManyField(Document, blank=True, verbose_name=_("default_code"), related_name='default_code')
    answers = models.ManyToManyField(Answer, blank=True, verbose_name=_("answers"))
    languages = models.ManyToManyField(Language, blank=True)
    can_add_documents = models.BooleanField(default=False)
    can_add_code = models.BooleanField(default=False)
    criterias = models.ManyToManyField(Criteria, blank=True,)
    evaluations = models.ForeignKey(Evaluation, related_name="evaluations", blank=True, null=True, on_delete=models.CASCADE)
    pair_evaluations = models.ManyToManyField(Evaluation, blank=True, verbose_name=_("evaluation by pair"), related_name='pair_evaluation')
    allow_pair_evaluation = models.BooleanField(_("Allow pair evaluation"), default=False)

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

    def get_data_docs(self):
        return [(d.name, d.get_buttons(self.doc_buttons)) for d in self.documents.all()]

    def get_data_codes(self):
        return [(d.name, d.get_buttons(self.code_buttons)) for d in self.default_code.all()]

    def get_data_answers(self):
        return [(a.user, a.get_buttons(self.answers_buttons)) for a in self.answers.all()]

    def get_data_criterias(self):
        return [(c.name, c.detail, c.max_points, c.step, c.get_buttons(self.criterias_buttons)) for c in self.criterias.all()]


class QuestionTests(models.Model):
    refer_question = models.ForeignKey(
        "question.Question", on_delete=models.CASCADE)
    path = models.FilePathField(
        path=settings.MEDIA_DIR, recursive=True, allow_folders=False, allow_files=True)
    command_execute = models.CharField(max_length=256, blank=False)
    command_list = models.CharField(max_length=256, blank=False)

    def __str__(self):
        return "Tests for " + str(self.refer_question)

    def get_test_names(self):
        cmd = (self.command_list + " " +
               os.path.join(settings.BASE_DIR, self.path)).split()
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _err = process.communicate()
        return self.parse_pytest_list(output.decode("utf-8"))

    def run_tests(self, answer):
        cmd = (self.command_execute + " " + os.path.join(
            settings.BASE_DIR, self.path)).split()
        process = subprocess.Popen(cmd, cwd=str(
            answer.path), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _err = process.communicate()
        # TODO: gérer les erreurs de syntaxe.
        return self.parse_pytest_output(out.decode("utf-8"))

    def parse_pytest_output(self, std_out):
        res = []
        for line in std_out.split("\n"):
            print(line)
            if "FAILED" in line or "PASSED" in line:
                data = line.split("::")[1][:-7]
                name, result = data.split()
                success = result == "PASSED"
                res.append(TestResult(name, success).to_json())
            if line.startswith("===========") and "FAILURES" in line:
                break
        return res

    def parse_pytest_list(self, output):
        res = []
        for line in output.split("\n"):
            line = line.strip()
            if line.startswith("<Function "):
                # Each line looks like <Function name_of_the_function>
                res.append(TestResult(line[10:-1], False))
        return res


class TestResult:
    def __init__(self, name, success):
        self.name = name
        self.success = success

    def __str__(self):
        return self.name + ": " + "OK" if self.success else "KO"

    def to_json(self):
        return self.__dict__
