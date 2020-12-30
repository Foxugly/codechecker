from django.contrib.auth.mixins import LoginRequiredMixin

from answer.forms import AnswerForm
from answer.models import Answer
from tools.generic_views import *


class AnswerCreateView(LoginRequiredMixin, GenericCreateView):
    model = Answer
    fields = None
    form_class = AnswerForm


class AnswerListView(LoginRequiredMixin, GenericListView):
    model = Answer
    template_name = 'list.html'


class AnswerUpdateView(LoginRequiredMixin, GenericUpdateView):
    model = Answer
    fields = None
    form_class = AnswerForm
    template_name = 'update.html'


class AnswerDetailView(LoginRequiredMixin, GenericDetailView):
    model = Answer


class AnswerDeleteView(LoginRequiredMixin, GenericDeleteView):
    model = Answer
