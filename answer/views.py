from django.contrib.auth.mixins import LoginRequiredMixin
from bootstrap_modal_forms.generic import BSModalReadView
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
import os

from document.models import Document
from language.models import Extension
from answer.forms import AnswerForm
from answer.models import Answer
from tools.generic_views import *
from django.utils.translation import gettext as _


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


class AnswerDocumentUploadView(LoginRequiredMixin, BSModalReadView):
    model = Answer
    template_name = 'modal_upload.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_doc = self.request.GET.get("type")
        title = _("Add code files") if type_doc == "code" else _("Add documents")
        action_url = "{0}?type={1}".format(reverse('answer:upload_document', kwargs={'pk': self.object.id}), type_doc)
        context.update({'title': title, 'action_url': action_url, "source": "answer"})
        return context


def file_upload_view(request, pk):
    a = Answer.objects.get(pk=pk)
    if request.method == 'POST':
        f = request.FILES.get('file')
        filename = f._name
        e = filename.split('.')[-1]
        ext = Extension.objects.all()[0]  # TODO
        doc = Document.objects.create(file=f, name=filename, extension=ext)
        path_filename = os.path.join(a.get_relative_path(request.user), filename)
        os.rename(doc.file.path, path_filename)
        doc.file.name = os.path.relpath(path_filename, settings.MEDIA_URL)
        doc.path = path_filename
        doc.save()
        a.docs.add(doc)
        a.save()
        return JsonResponse({'filename': doc.name, 'buttons': doc.get_button_download_delete()})
    return JsonResponse({'post': 'false'})
