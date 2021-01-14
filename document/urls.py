from django.urls import path
from tools.generic_urls import add_url_from_generic_views
from .views import DocumentPopupDeleteView

app_name = 'document'
urlpatterns = [
    path('document/<int:pk>/popup/delete/', DocumentPopupDeleteView.as_view(), name='document_popup_delete'),
]

urlpatterns += add_url_from_generic_views('document.views')
