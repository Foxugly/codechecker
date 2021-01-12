from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.urls import reverse
from chapter.forms import ChapterForm, ChapterPopupCreateForm
from chapter.models import Chapter
from tools.generic_views import *
from bootstrap_modal_forms.generic import BSModalCreateView
from course.models import Course


class ChapterPopupCreateView(LoginRequiredMixin, BSModalCreateView):
    model = Chapter
    form_class = ChapterPopupCreateForm
    template_name = 'document_popup.html'
    refer_course = None
    success_url = None

    def get_initial(self):
        if self.request.GET.get('course_id'):
            self.refer_course = self.request.GET.get('course_id')
        return super().get_initial()

    def form_valid(self, form):
        if not self.request.is_ajax():
            course = Course.objects.get(id=self.refer_course)
            form.instance.refer_course = course
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Add chapter")
        return context

    def get_success_url(self):
        if not self.request.is_ajax():
            return reverse('chapter:chapter_detail', kwargs={'pk': self.object.id})
        else:
            return reverse('home')



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
        context['treeview'] = self.object.refer_course.get_json()
        return context


class ChapterDeleteView(LoginRequiredMixin, GenericDeleteView):
    model = Chapter
