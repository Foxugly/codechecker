from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from users.forms import UserForm
from users.models import User
from tools.generic_views import *


class ProfileUpdateView(GenericUpdateView):
    model = User
    fields = None
    form_class = UserForm
    template_name = 'update.html'
    success_url = reverse_lazy('users:profile_update')
    success_message = _('Changes saved.')

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        context.update({'title': _("Mise à jour de mon profil")})
        return context
