from django import forms
from codes.models import Category, Code


class CreateCodeForm(forms.Form):
    """
    A form to manage the creation of codes from the admin.
    """
    def __init__(self, event, *args, **kwargs):
        """
        Dynamically add a field per each category in the db.
        """
        super(CreateCodeForm, self).__init__(*args, **kwargs)
        self.event = event
        self._created_codes = False  # A flag to prevent multiple processing of the same form
        for idx, category in enumerate(Category.objects.all()):
            self.fields["category_%s" % (idx + 1)] = forms.IntegerField(label=category.name)

    def create_codes(self):
        """
        Create ``Code`` objects based on the values entered via the form.
        """
        if self.is_valid() and not self._created_codes:
            def get_category(field_name):
                return Category.objects.get(pk=int(field_name.split("_")[-1]))

            for field in self.cleaned_data:
                for idx in range(self.cleaned_data[field]):
                    Code.objects.create(category=get_category(field),
                                        event=self.event)

            self._created_codes = True  # Prevent the form from being processed more than once