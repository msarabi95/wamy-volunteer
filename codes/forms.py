# coding=utf-8
from django import forms
from django.contrib import messages
from django.utils import timezone
from codes.models import Category, Code, Order, CODE_STRING_LENGTH


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

            order = Order.objects.create(event=self.event)

            for field in self.cleaned_data:
                for idx in range(self.cleaned_data[field]):
                    Code.objects.create(category=get_category(field),
                                        event=self.event,
                                        order=order)

            self._created_codes = True  # Prevent the form from being processed more than once


class RedeemCodeForm(forms.Form):
    string = forms.CharField(max_length=CODE_STRING_LENGTH)

    def __init__(self, user, *args, **kwargs):
        super(RedeemCodeForm, self).__init__(*args, **kwargs)
        self.user = user  # Save the user as this is important for validation

    def clean_string(self):
        """
        Check that:
        (1) code exists.
        (2) code is available.
        (3) user doesn't have another code in the same event.
        """
        code_string = self.cleaned_data['string']

        # first, check that code exists
        if not Code.objects.filter(string=code_string).exists():
            raise forms.ValidationError("Code does not exist.", code="DoesNotExist")
        else:
            code = Code.objects.get(string=code_string)
            # next, check that code is available
            if code.user is not None:
                raise forms.ValidationError("Code is not available.", code="Unavailable")
            else:
                # finally, check that user doesn't have another code in the same event
                if Code.objects.filter(event=code.event, user=self.user).exists():  # and not code.event.allow_multiple:
                    raise forms.ValidationError("User has another code in the same event.", code="HasOtherCode")

        return code_string

    def process(self):
        """
        Register the submitted code for the submitting user if the submission is valid; otherwise do nothing.
        In both cases, return an appropriate message.
        :return: a tuple containing a message type and a message.
        """
        if self.is_valid():
            code = Code.objects.get(string=self.cleaned_data['string'])
            code.user = self.user
            code.date_redeemed = timezone.now()
            code.save()

            message = u"تم إدخال الرمز بنجاح."
            message_type = messages.SUCCESS

        else:
            message = u"حصل خطأ ما."
            message_type = messages.ERROR

            print self.fields['string'].errors.as_data()

        return (message_type, message)