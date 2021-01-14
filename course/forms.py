from django.forms import ModelForm

from course.models import Course

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CourseForm(ModelForm):
    model = Course

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.form_class = "form-horizontal"
        self.helper.add_input(Submit('submit', 'Save'))

    class Meta:
        model = Course
        fields = ['name', 'slug', 'year', 'description']
