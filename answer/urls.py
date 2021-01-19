from django.urls import path

from answer.ajax import get_content, set_content, get_default_content, add_file, execute_anwser, run_tests
from tools.generic_urls import add_url_from_generic_views
from .views import AnswerDocumentUploadView, file_upload_view

app_name = 'answer'
urlpatterns = [
    path('answer/<int:document_id>/get_content/',
         get_content, name='answer_get_content'),
    path('answer/<int:document_id>/set_content/',
         set_content, name='answer_set_content'),
    path('answer/<int:document_id>/get_default_content/',
         get_default_content, name='answer_get_default_content'),
    path('answer/<int:answer_id>/add_file', add_file, name='answer_add_file'),
    path('answer/<int:answer_id>/execute',
         execute_anwser, name='answer_execute'),
    path('answer/<int:answer_id>/test', run_tests, name='answer_test'),
    path('answer/<int:pk>/document/popup/add/',
         AnswerDocumentUploadView.as_view(), name='document_popup_add'),
    path('answer/<int:pk>/document/upload',
         file_upload_view, name='upload_document'),
]

urlpatterns += add_url_from_generic_views('answer.views')
