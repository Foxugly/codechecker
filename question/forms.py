from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Button, Submit, HTML
from django.forms import ModelForm
from django import forms

from answer.models import Answer
from question.models import Question
from language.models import Language
from tinymce.widgets import TinyMCE


class QuestionForm(ModelForm):
    question = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['languages'].widget.attrs['class'] = 'select2'
        if self.instance:
            self.fields['answers'].widget = forms.CheckboxSelectMultiple(attrs={'class':"striped-list"})
            self.fields['answers'].queryset = self.instance.answers.all()


            self.fields['default_code'].widget = forms.CheckboxSelectMultiple(attrs={'class':"striped-list"})
            self.fields['default_code'].queryset = self.instance.default_code.all()

            self.fields['documents'].widget = forms.CheckboxSelectMultiple(attrs={'class':"striped-list"})
            self.fields['documents'].queryset = self.instance.documents.all()
        self.helper = FormHelper(self)
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.form_class = "form-horizontal"

        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.add_input(Button('cancel', 'Cancel', onclick='window.location.href="/"'))

    class Meta:
        model = Question
        fields = '__all__'