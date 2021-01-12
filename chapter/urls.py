from tools.generic_urls import add_url_from_generic_views
from .views import ChapterPopupCreateView
from django.urls import path

app_name = 'chapter'
urlpatterns = [
    path('chapter/popup/add/', ChapterPopupCreateView.as_view(), name='chapter_popup_add'),
]

urlpatterns += add_url_from_generic_views('chapter.views')
