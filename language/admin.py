from django.contrib import admin

from language.models import Language, Extension


class LanguageAdmin(admin.ModelAdmin):
    pass


class ExtensionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Language, LanguageAdmin)
admin.site.register(Extension, ExtensionAdmin)
