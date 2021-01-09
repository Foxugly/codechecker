from django.urls import path

from answer.ajax import get_content, set_content, get_default_content, add_file, execute_anwser
from tools.generic_urls import add_url_from_generic_views

app_name = 'answer'
urlpatterns = [
    path('answer/<int:document_id>/get_content/', get_content, name='answer_get_content'),
    path('answer/<int:document_id>/set_content/', set_content, name='answer_set_content'),
    path('answer/<int:document_id>/get_default_content/', get_default_content, name='answer_get_default_content'),
    path('answer/<int:answer_id>/add_file', add_file, name='answer_add_file'),
    path('answer/<int:answer_id>/execute', execute_anwser, name='answer_execute')
]

urlpatterns += add_url_from_generic_views('answer.views')
