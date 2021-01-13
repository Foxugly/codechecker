from tools.generic_urls import add_url_from_generic_views
from .views import QuestionPopupCreateView, QuestionDocumentUploadView, file_upload_view
from django.urls import path

app_name = 'question'
urlpatterns = [
    path('question/<int:pk>/document/popup/add/', QuestionDocumentUploadView.as_view(), name='document_popup_add'),
    path('question/<int:pk>/document/upload', file_upload_view, name='upload_document'),
    path('popup/add/', QuestionPopupCreateView.as_view(), name='question_popup_add'),
]

urlpatterns += add_url_from_generic_views('question.views')
