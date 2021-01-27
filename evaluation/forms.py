from bootstrap_modal_forms.forms import BSModalModelForm
from evaluation.models import Criteria


class CriteriaPopupForm(BSModalModelForm):

    class Meta:
        model = Criteria
        fields = ('name', 'detail', 'max_points', 'step')
