from tools.generic_urls import add_url_from_generic_views
from .views import QuestionPopupCreateView, DocumentUploadView, file_upload_view
from evaluation.views import CriteriaCreateView
from django.urls import path

app_name = 'question'
urlpatterns = [
    path('question/<int:pk>/document/popup/add/', DocumentUploadView.as_view(), name='document_popup_add'),
    path('question/<int:pk>/criteria/popup/add/', CriteriaCreateView.as_view(), name='criteria_popup_add'),
    path('question/<int:pk>/document/upload', file_upload_view, name='upload_document'),
    path('popup/add/', QuestionPopupCreateView.as_view(), name='question_popup_add'),


]

urlpatterns += add_url_from_generic_views('question.views')
