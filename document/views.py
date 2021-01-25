from django.contrib.auth.mixins import LoginRequiredMixin

from document.forms import DocumentForm, DocumentPopupCreateForm
from document.models import Document
from tools.generic_views import *
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalReadView
from django.utils.translation import gettext as _
from django.http import HttpResponse
import json


class DocumentCreateView(LoginRequiredMixin, GenericCreateView):
    model = Document
    fields = None
    form_class = DocumentForm
    template_name = 'update.html'


class DocumentListView(LoginRequiredMixin, GenericListView):
    model = Document
    template_name = 'list.html'


class DocumentUpdateView(LoginRequiredMixin, GenericUpdateView):
    model = Document
    fields = None
    form_class = DocumentForm
    template_name = 'update.html'


class DocumentDetailView(LoginRequiredMixin, GenericDetailView):
    model = Document
    template_name = 'detail.html'


class DocumentDeleteView(LoginRequiredMixin, GenericDeleteView):
    model = Document


class DocumentUploadView(LoginRequiredMixin, BSModalReadView):
    model = Document
    template_name = 'modal_upload.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': _("Add documents"), 'type': self.request.GET.get("type")})
        return context


def document_ajax_delete(request, document_id):
    results = {}
    if request.is_ajax():
        try:
            doc = Document.objects.get(pk=document_id)
            results['valid'] = doc.delete()
        except Document.DoesNotExist:
            results['valid'] = False
            results['error'] = "unknown document_id"
    else:
        results['valid'] = False
        results['error'] = "request is not ajax"
    return HttpResponse(json.dumps(results))
