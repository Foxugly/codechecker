from django.contrib import admin
from django.utils.translation import gettext as _

from users.models import User


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('netid', 'email', 'first_name', 'last_name', 'is_staff', 'is_academic',)
    list_filter = ('is_staff', 'is_academic',)
    fieldsets = (
        (_('Personal info'), {'fields': ('netid', 'email', 'first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_staff', 'is_academic',)}),
        (_('Courses'), {'fields': ('courses', 'moderated_courses')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )
    search_fields = ('netid', 'email', 'first_name', 'last_name',)
    ordering = ('netid',)
    filter_horizontal = ('courses', 'moderated_courses')


admin.site.register(User, CustomUserAdmin)
