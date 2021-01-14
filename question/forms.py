from django import forms
from django.forms import ModelForm
from question.models import Question
from tinymce.widgets import TinyMCE
from bootstrap_modal_forms.forms import BSModalModelForm


class QuestionPopupCreateForm(BSModalModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['name', ]


class QuestionUpdateForm(ModelForm):
    question = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))

    class Meta:
        model = Question
        fields = ['name', 'question', 'can_add_documents', 'languages', 'can_add_code', 'answers']


class QuestionCreateForm(ModelForm):
    question = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['languages'].widget.attrs['class'] = 'select2'

    class Meta:
        model = Question
        fields = ['name', 'question', 'can_add_documents', 'languages', 'can_add_code', ]
