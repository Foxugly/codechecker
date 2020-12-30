from django.contrib import admin

from question.models import Question


class QuestionAdmin(admin.ModelAdmin):
    filter_horizontal = ('documents', 'default_code', 'answers', 'languages')


admin.site.register(Question, QuestionAdmin)
