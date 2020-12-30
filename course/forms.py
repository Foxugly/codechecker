from django.forms import ModelForm

from course.models import Course


class CourseForm(ModelForm):
    model = Course

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Course
        fields = ['slug', ]
