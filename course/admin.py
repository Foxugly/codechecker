from django.contrib import admin

from course.models import Course


class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ('chapters',)


admin.site.register(Course, CourseAdmin)
