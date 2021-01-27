from django.contrib.auth.mixins import LoginRequiredMixin

from evaluation.forms import CriteriaPopupForm
from evaluation.models import Evaluation, Criteria
from tools.generic_views import *
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalReadView, BSModalUpdateView
from django.utils.translation import gettext as _
from django.http import HttpResponse
from question.models import Question
from django.urls import reverse
import json


def criteria_ajax_delete(request, criteria_id):
    results = {}
    if request.is_ajax():
        try:
            doc = Criteria.objects.get(pk=criteria_id)
            results['valid'] = doc.delete()
        except Criteria.DoesNotExist:
            results['valid'] = False
            results['error'] = "unknown criteria_id"
    else:
        results['valid'] = False
        results['error'] = "request is not ajax"
    return HttpResponse(json.dumps(results))


class CriteriaCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'modal_form.html'
    form_class = CriteriaPopupForm
    success_message = 'Success: Criteria was created.'
    success_url = "/"

    def get_initial(self):
        if self.kwargs['pk']:
            self.refer_question = Question.objects.get(pk=self.kwargs['pk'])
        return super().get_initial()

    def form_valid(self, form):
        if not self.request.is_ajax():
            form.instance.refer_question = Question.objects.get(id=self.refer_question.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Add criteria")
        context['btn_label'] = _("Add")
        return context

    def get_success_url(self):
        if not self.request.is_ajax():
            return reverse('question:question_change', kwargs={'pk': self.refer_question.id})
        else:
            return reverse('home')


class CriteriaListView(LoginRequiredMixin, GenericListView):
    model = Criteria
    template_name = 'list.html'


class CriteriaUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Criteria
    form_class = CriteriaPopupForm
    template_name = 'modal_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = _("Update criteria")
        context['btn_label'] = _("Update")
        return context

    def get_success_url(self):
        if not self.request.is_ajax():
            return reverse('question:question_change', kwargs={'pk': self.refer_question.id})
        else:
            return reverse('home')


class CriteriaDetailView(LoginRequiredMixin, GenericDetailView):
    model = Criteria
    template_name = 'detail.html'


class CriteriaDeleteView(LoginRequiredMixin, GenericDeleteView):
    model = Criteria


