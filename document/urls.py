from django.urls import path
from tools.generic_urls import add_url_from_generic_views
from .views import DocumentPopupCreateView

app_name = 'document'
urlpatterns = [
    path('document/popup/add/', DocumentPopupCreateView.as_view(), name='document_popup_add'),
]

urlpatterns += add_url_from_generic_views('document.views')

