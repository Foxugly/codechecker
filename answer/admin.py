from django.contrib import admin

from answer.models import Answer


class AnswerAdmin(admin.ModelAdmin):
    filter_horizontal = ('code',)


admin.site.register(Answer, AnswerAdmin)
