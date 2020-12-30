from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _

from chapter.forms import ChapterForm
from chapter.models import Chapter
from tools.generic_views import *


class ChapterCreateView(LoginRequiredMixin, GenericCreateView):
    model = Chapter
    fields = None
    form_class = ChapterForm
    success_message = _('Cours ajouté.')


class ChapterListView(LoginRequiredMixin, GenericListView):
    model = Chapter


class ChapterUpdateView(LoginRequiredMixin, GenericUpdateView):
    model = Chapter
    fields = None
    form_class = ChapterForm
    template_name = 'index.html'


class ChapterDetailView(LoginRequiredMixin, GenericDetailView):
    model = Chapter
    template_name = 'detail_chapter.html'

    def get_context_data(self, **kwargs):
        context = super(ChapterDetailView, self).get_context_data(**kwargs)
        context['treeview'] = self.object.get_json()
        return context


class ChapterDeleteView(LoginRequiredMixin, GenericDeleteView):
    model = Chapter
