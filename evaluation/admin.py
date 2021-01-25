from django.contrib import admin

from .models import Criteria, Evaluation


class CriteriaAdmin(admin.ModelAdmin):
    pass


class EvaluationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Criteria, CriteriaAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
