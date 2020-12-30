from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from django.forms import ModelForm

from answer.models import Answer


class AnswerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.form_class = "form-horizontal"
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.add_input(Button('cancel', 'Cancel', onclick='window.location.href="/"'))

    class Meta:
        model = Answer
        fields = '__all__'
