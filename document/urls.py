from django.urls import path
from tools.generic_urls import add_url_from_generic_views
from .views import document_ajax_delete

app_name = 'document'
urlpatterns = [
    path('document/<int:document_id>/ajax/delete/', document_ajax_delete, name='document_ajax_delete'),
]

urlpatterns += add_url_from_generic_views('document.views')
