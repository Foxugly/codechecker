from django.urls import path

from tools.generic_urls import add_url_from_generic_views
from users.profile_views import ProfileUpdateView

app_name = 'users'

urlpatterns = [
                  path('profile/', ProfileUpdateView.as_view(), name='profile_update'),
              ] + add_url_from_generic_views('users.views')
