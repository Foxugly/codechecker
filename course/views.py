from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _

from course.forms import CourseForm
from course.models import Course
from tools.generic_views import *


class CourseCreateView(LoginRequiredMixin, GenericCreateView):
    model = Course
    fields = None
    form_class = CourseForm
    success_message = _('Cours ajouté.')


class CourseListView(LoginRequiredMixin, GenericListView):
    model = Course


class CourseUpdateView(LoginRequiredMixin, GenericUpdateView):
    model = Course
    fields = None
    form_class = CourseForm
    template_name = 'update.html'


class CourseDetailView(LoginRequiredMixin, GenericDetailView):
    model = Course
    template_name = 'detail_course.html'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['treeview'] = self.object.get_json()
        return context


class CourseDeleteView(LoginRequiredMixin, GenericDeleteView):
    model = Course
