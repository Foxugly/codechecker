from tools.generic_urls import add_url_from_generic_views

app_name = 'document'
urlpatterns = []

urlpatterns += add_url_from_generic_views('document.views')

