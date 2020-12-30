from django.forms import ModelForm

from chapter.models import Chapter


class ChapterForm(ModelForm):
    model = Chapter

    def __init__(self, *args, **kwargs):
        super(ChapterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Chapter
        fields = ['slug', ]
