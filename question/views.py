from django.contrib.auth.mixins import LoginRequiredMixin

from answer.models import Answer
from document.forms import DocumentForm
from question.forms import QuestionCreateForm, QuestionUpdateForm, QuestionPopupCreateForm
from question.models import Question
from tools.generic_views import *
from chapter.models import Chapter
from bootstrap_modal_forms.generic import BSModalCreateView
from django.utils.translation import gettext as _
from django.urls import reverse


class QuestionPopupCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Question
    form_class = QuestionPopupCreateForm
    template_name = 'document_popup.html'
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


class QuestionDetailView(LoginRequiredMixin, GenericDetailView):
    model = Question
    template_name = 'detail_question.html'

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
