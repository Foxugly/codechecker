from django.forms import ModelForm

from document.models import Document


class DocumentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = "form-control"
        self.fields['name'].widget.attrs['placeholder'] = "filename"
        self.fields['extension'].widget.attrs['class'] = "form-select"

    class Meta:
        model = Document
        fields = ('name', 'extension')
