from django.contrib.auth.forms import UserChangeForm

from users.models import User


class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
