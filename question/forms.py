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
        doc_btns, code_btns, answers_btns = kwargs.pop('doc_btns'), kwargs.pop('code_btns'), kwargs.pop('answers_btns')
        super().__init__(*args, **kwargs)
        self.fields['languages'].widget.attrs['class'] = 'select2'
        if self.instance:
            self.fields['answers'].widget = TableWidget(choices=self.instance.answers.all(), buttons=answers_btns)
            self.fields['documents'].widget = TableWidget(choices=self.instance.documents.all(), buttons=doc_btns)
            self.fields['default_code'].widget = TableWidget(choices=self.instance.default_code.all(), buttons=code_btns)
        else:
            self.fields['documents'].widget = TableWidget(buttons=doc_btns)
            self.fields['default_code'].widget = TableWidget(buttons=code_btns)
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
        doc_btns, code_btns = kwargs.pop('doc_btns'), kwargs.pop('code_btns')
        super().__init__(*args, **kwargs)
        self.fields['languages'].widget.attrs['class'] = 'select2'
        self.fields['documents'].widget = TableWidget(buttons=doc_btns)
        self.fields['default_code'].widget = TableWidget(buttons=code_btns)
        self.helper = FormHelper(self)
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.form_class = "form-horizontal"

        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.add_input(Button('cancel', 'Cancel', onclick='window.location.href="/"'))

    class Meta:
        model = Question
        fields = ['name', 'question', 'documents', 'can_add_documents', 'languages', 'default_code', 'can_add_code', ]
