from django.contrib import admin

from answer.models import Answer


class AnswerAdmin(admin.ModelAdmin):
    filter_horizontal = ('codes', 'docs')


admin.site.register(Answer, AnswerAdmin)
