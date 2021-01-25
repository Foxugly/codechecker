from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Button, Submit, HTML
from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from django.forms import ModelForm
from document.models import Document
from tinymce.widgets import TinyMCE


class DocumentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = "form-control"
        self.fields['name'].widget.attrs['placeholder'] = "filename"
        self.fields['extension'].widget.attrs['class'] = "form-select"

    class Meta:
        model = Document
        fields = ('name', 'extension')


class DocumentPopupCreateForm(BSModalModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = "form-control"
        self.fields['name'].widget.attrs['placeholder'] = "filename"
        #self.fields['extension'].widget.attrs['class'] = "form-select"
        self.helper = FormHelper(self)
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.form_class = "form-horizontal"

    class Meta:
        model = Document
        fields = ('name', 'extension')