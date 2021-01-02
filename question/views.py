from django.contrib.auth.mixins import LoginRequiredMixin

from answer.models import Answer
from document.forms import DocumentForm
from question.forms import QuestionForm
from question.models import Question
from tools.generic_views import *


class QuestionCreateView(LoginRequiredMixin, GenericCreateView):
    model = Question
    fields = None
    form_class = QuestionForm



class QuestionListView(LoginRequiredMixin, GenericListView):
    model = Question
    template_name = 'list.html'


class QuestionUpdateView(LoginRequiredMixin, GenericUpdateView):
    model = Question
    fields = None
    form_class = QuestionForm
    template_name = 'update_question.html'


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
