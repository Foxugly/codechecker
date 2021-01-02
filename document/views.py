from django.contrib.auth.mixins import LoginRequiredMixin

from document.forms import DocumentForm
from document.models import Document
from tools.generic_views import *


class DocumentCreateView(LoginRequiredMixin, GenericCreateView):
    model = Document
    fields = None
    form_class = DocumentForm



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
