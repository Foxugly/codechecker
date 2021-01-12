from django.forms import widgets


class TableWidget(widgets.ChoiceWidget):
    allow_multiple_selected = True
    input_type = 'select'
    template_name = 'widgets/checkbox_select.html'
    option_template_name = 'widgets/checkbox_option.html'

    def __init__(self, attrs=None, choices=(), buttons=(), add_url="/"):
        super().__init__(attrs)
        self.queryset = list(choices)
        self.buttons = list(buttons)
        self.add_url = add_url

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['queryset'] = self.queryset
        context['buttons'] = self.buttons
        context['add_url'] = self.add_url
        return context