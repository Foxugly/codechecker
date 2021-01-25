from django.urls import path
from evaluation.views import CriteriaCreateView, CriteriaDetailView, CriteriaUpdateView, CriteriaDeleteView, criteria_ajax_delete

app_name = 'evaluation'
urlpatterns = [
    path('criteria/add/', CriteriaCreateView.as_view(), name='criteria_add'),
    path('criteria/<int:pk>/change/', CriteriaUpdateView.as_view(), name='criteria_change'),
    path('criteria/<int:pk>/', CriteriaDetailView.as_view(), name='criteria_detail'),
    path('criteria/<int:pk>/delete/', CriteriaDeleteView.as_view(), name='criteria_delete'),
    path('criteria/<int:pk>/delete/', CriteriaDeleteView.as_view(), name='criteria_delete'),
    path('criteria/<int:criteria_id>/ajax/delete/', criteria_ajax_delete, name='criteria_ajax_delete'),
]


