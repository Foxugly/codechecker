from django.urls import path
from tools.generic_urls import add_url_from_generic_views
from .views import DocumentUploadView

app_name = 'document'
urlpatterns = []

urlpatterns += add_url_from_generic_views('document.views')

