from users.models import User
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


class UserLoginView(LoginView):
    model = User
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
