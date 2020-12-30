from tools.generic_urls import add_url_from_generic_views

app_name = 'question'
urlpatterns = []

urlpatterns += add_url_from_generic_views('question.views')
