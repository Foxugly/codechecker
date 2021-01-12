from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit

from django import forms
from django.forms import ModelForm
from question.models import Question
from tinymce.widgets import TinyMCE
from bootstrap_modal_forms.forms import BSModalModelForm
from tools.widgets import TableWidget


class QuestionPopupCreateForm(BSModalModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['name', ]


class QuestionUpdateForm(ModelForm):
    question = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['languages'].widget.attrs['class'] = 'select2'
        if self.instance:
            choices, buttons = self.instance.answers.all(), ['detail', 'delete']
            self.fields['answers'].widget = TableWidget(choices=choices, buttons=buttons)
            choices, buttons = self.instance.documents.all(), ['add', 'detail', 'download', 'delete']
            self.fields['documents'].widget = TableWidget(choices=choices, buttons=buttons)
            choices, buttons = self.instance.default_code.all(), ['add', 'detail', 'download', 'delete']
            self.fields['default_code'].widget = TableWidget(choices=choices, buttons=buttons)

        self.helper = FormHelper(self)
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.form_class = "form-horizontal"

        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.add_input(Button('cancel', 'Cancel', onclick='window.location.href="/"'))

    class Meta:
        model = Question
        fields = ['name', 'question', 'documents', 'can_add_documents', 'languages', 'default_code', 'can_add_code', 'answers']


class QuestionCreateForm(ModelForm):
    question = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['languages'].widget.attrs['class'] = 'select2'
        self.fields['documents'].widget = TableWidget(buttons=['add', 'detail', 'download', 'delete'],)
        self.fields['default_code'].widget = TableWidget(buttons=['add', 'detail', 'download', 'delete'],)
        self.helper = FormHelper(self)
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.form_class = "form-horizontal"

        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.add_input(Button('cancel', 'Cancel', onclick='window.location.href="/"'))

    class Meta:
        model = Question
        fields = ['name', 'question', 'documents', 'can_add_documents', 'languages', 'default_code', 'can_add_code', ]
