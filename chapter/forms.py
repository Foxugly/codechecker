from django.forms import ModelForm
from bootstrap_modal_forms.forms import BSModalModelForm
from chapter.models import Chapter


class ChapterPopupCreateForm(BSModalModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Chapter
        fields = ['name', ]


class ChapterForm(ModelForm):
    model = Chapter

    def __init__(self, *args, **kwargs):
        super(ChapterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Chapter
        fields = ['slug', ]
