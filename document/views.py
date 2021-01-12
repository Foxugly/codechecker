from django.contrib.auth.mixins import LoginRequiredMixin

from document.forms import DocumentForm, DocumentPopupCreateForm
from document.models import Document
from tools.generic_views import *
from bootstrap_modal_forms.generic import BSModalCreateView
from django.utils.translation import gettext as _


class DocumentPopupCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Document
    fields = None
    form_class = DocumentPopupCreateForm
    template_name = 'document_popup.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': _("Add qqch")})
        return context


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
