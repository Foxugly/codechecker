from django.contrib import admin

from question.models import Question, QuestionTests


class QuestionAdmin(admin.ModelAdmin):
    filter_horizontal = ('documents', 'default_code', 'answers', 'languages', 'criterias')


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionTests)
