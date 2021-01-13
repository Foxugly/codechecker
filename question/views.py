from django.contrib.auth.mixins import LoginRequiredMixin

from answer.models import Answer
from document.forms import DocumentForm
from question.forms import QuestionCreateForm, QuestionUpdateForm, QuestionPopupCreateForm
from question.models import Question
from tools.generic_views import *
from chapter.models import Chapter
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalReadView
from django.utils.translation import gettext as _
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from document.models import Document
from language.models import Extension
from django.conf import settings
import os


class QuestionPopupCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Question
    form_class = QuestionPopupCreateForm
    template_name = 'form_popup.html'
    refer_course = None
    success_url = None

    def get_initial(self):
        if self.request.GET.get('chapter_id'):
            self.refer_chapter = self.request.GET.get('chapter_id')
        return super().get_initial()

    def form_valid(self, form):
        if not self.request.is_ajax():
            form.instance.refer_chapter = Chapter.objects.get(id=self.refer_chapter)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Add Question")
        return context

    def get_success_url(self):
        if not self.request.is_ajax():
            return reverse('question:question_change', kwargs={'pk': self.object.id})
        else:
            return reverse('home')


class QuestionCreateView(LoginRequiredMixin, GenericCreateView):
    model = Question
    fields = None
    form_class = QuestionCreateForm

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super().get_form_kwargs(**kwargs)
        form_kwargs["doc_btns"] = Question.doc_buttons
        form_kwargs["code_btns"] = Question.code_buttons
        form_kwargs["answers_btns"] = Question.answers_buttons
        return form_kwargs


class QuestionListView(LoginRequiredMixin, GenericListView):
    model = Question
    template_name = 'list.html'


class QuestionUpdateView(LoginRequiredMixin, GenericUpdateView):
    model = Question
    fields = None
    form_class = QuestionUpdateForm
    template_name = 'update_question.html'

    def get_success_url(self):
        return reverse('chapter:chapter_detail', kwargs={'pk': self.object.refer_chapter.id})

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super().get_form_kwargs(**kwargs)
        form_kwargs["doc_btns"] = Question.doc_buttons
        form_kwargs["code_btns"] = Question.code_buttons
        form_kwargs["answers_btns"] = Question.answers_buttons
        return form_kwargs


class QuestionDetailView(LoginRequiredMixin, GenericDetailView):
    model = Question
    template_name = 'detail_question.html'

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super().get_form_kwargs(**kwargs)
        form_kwargs["doc_btns"] = Question.doc_buttons
        form_kwargs["code_btns"] = Question.code_buttons
        form_kwargs["answers_btns"] = Question.answers_buttons
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super(GenericDetailView, self).get_context_data(**kwargs)
        context['treeview'] = self.object.refer_chapter.refer_course.get_json()
        context['course'] = self.object.refer_chapter.refer_course
        answer = Answer.objects.get(refer_question=self.object, user=self.request.user)
        context["answer"] = answer
        context['mode'] = answer.code.all()[0].extension.mode
        context['documentForm'] = DocumentForm()
        return context


class QuestionDeleteView(LoginRequiredMixin, GenericDeleteView):
    model = Question


class QuestionDocumentUploadView(LoginRequiredMixin, BSModalReadView):
    model = Question
    template_name = 'form_upload.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_doc = self.request.GET.get("type")
        title = _("Add code files") if type_doc == "code" else _("Add documents")
        action_url = "{0}?type={1}".format(reverse('question:upload_document', kwargs={'pk': self.object.id}), type_doc)
        print(action_url)
        context.update({'title': title, 'action_url': action_url})
        return context


def file_upload_view(request, pk):
    print(request)
    q = Question.objects.get(pk=pk)
    if request.method == 'POST':
        f = request.FILES.get('file')
        filename = f._name
        e = filename.split('.')[-1]
        print(e)
        ext = Extension.objects.all()[0]  # TODO
        doc = Document.objects.create(file=f, name=filename, extension=ext)
        path_filename = os.path.join(q.get_relative_path(), filename)
        os.rename(doc.file.path, path_filename)
        doc.file.name = os.path.relpath(path_filename, settings.MEDIA_URL)
        doc.path = path_filename
        doc.save()
        if request.GET.get("type") == "doc":
            q.documents.add(doc)
            list_buttons = q.doc_buttons
        else:
            q.default_code.add(doc)
            list_buttons = q.code_buttons
            buttons = '<a class="btn"></a>'
        buttons = ""
        for btn in list_buttons:
            if btn == "detail":
                buttons += '<a role="button" class="btn btn-sm btn-primary ml-1" href="{0}"><i class="far fa-eye"></i></a>'.format(doc.get_absolute_url())
            elif btn == "change":
                buttons += '<a role="button" class="btn btn-sm btn-info  ml-1" href="{0}"><i class="fas fa-edit"></i></a>'.format(doc.get_change_url())
            elif btn == "download":
                buttons += '<a role="button" class="btn btn-sm btn-success  ml-1" href="{0}"><i class="fas fa-download"></i></a>'.format(doc.get_download_url())
            elif btn == "delete":
                buttons += '<a role="button" class="btn btn-sm btn-danger ml-1" href="{0}"><i class="far fa-trash-alt"></i></a>'.format(doc.get_delete_url())
        q.save()
        return JsonResponse({'filename': doc.name, 'type': request.GET.get("type"), 'buttons': buttons})
    return JsonResponse({'post': 'false'})
