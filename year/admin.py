from django.contrib import admin

from year.models import Year


class YearAdmin(admin.ModelAdmin):
    pass


admin.site.register(Year, YearAdmin)
