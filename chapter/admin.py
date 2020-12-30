from django.contrib import admin

from chapter.models import Chapter


class ChapterAdmin(admin.ModelAdmin):
    filter_horizontal = ('questions',)


admin.site.register(Chapter, ChapterAdmin)
