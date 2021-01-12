from tools.generic_urls import add_url_from_generic_views
from .views import CourseDetailView, CourseListView
from django.urls import path
app_name = 'course'

urlpatterns = [
    path('', CourseListView.as_view(), name="course_list2"),
    path('<slug:slug>/', CourseDetailView.as_view(), name="course_slug_detail")

] + add_url_from_generic_views('course.views')
