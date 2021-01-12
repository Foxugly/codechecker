from tools.generic_urls import add_url_from_generic_views
from .views import QuestionPopupCreateView
from django.urls import path

app_name = 'question'
urlpatterns = [
    path('chapter/popup/add/', QuestionPopupCreateView.as_view(), name='question_popup_add'),
]

urlpatterns += add_url_from_generic_views('question.views')
