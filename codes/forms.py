# coding=utf-8
from django import forms
from django.contrib import messages
from django.utils import timezone
from codes.models import Category, Code, Order


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
            self.fields["category_%s" % (idx + 1)] = forms.IntegerField(label=category.name, required=False)
            # `clean()` (below) will make sure that at least one field has a non-zero value.

    def clean(self):
        """
        Make sure that at least one category has a non-zero value.
        """
        cleaned_data = super(CreateCodeForm, self).clean()

        # If all the values are either 0's or None's (no non-zero values), raise a validation error
        if all([(cleaned_data[field] is None or cleaned_data[field] == 0) for field in cleaned_data]):
            raise forms.ValidationError(u"أدخل، على الأقل، قيمة واحدة أكبر من الصفر.")

        # Replace None's with 0's
        for field in cleaned_data:
            if cleaned_data[field] is None:
                cleaned_data[field] = 0

        return cleaned_data

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
    string = forms.CharField(label="")

    def __init__(self, user, *args, **kwargs):
        super(RedeemCodeForm, self).__init__(*args, **kwargs)
        self.user = user  # Save the user as this is important for validation
        self.fields['string'].widget.attrs = {"class": "form-control input-lg input-wide english-field", "placeholder": u"أدخل رمزًا..."}

    def clean_string(self):
        """
        Check that:
        (1) code exists.
        (2) code is available.
        (3) user doesn't have another code in the same event.
        """
        # Make sure the code is uppercase, without any spaces or hyphens
        code_string = self.cleaned_data['string'].upper().replace(" ", "").replace("-", "")

        # first, check that code exists
        if not Code.objects.filter(string=code_string).exists():
            raise forms.ValidationError(u"هذا الرمز غير صحيح.", code="DoesNotExist")
        else:
            code = Code.objects.get(string=code_string)
            # next, check that code is available
            if code.user is not None:
                raise forms.ValidationError(u"هذا الرمز غير متوفر.", code="Unavailable")
            else:
                # finally, check that user doesn't have another code in the same event
                if Code.objects.filter(event=code.event, user=self.user).exists():  # and not code.event.allow_multiple:
                    raise forms.ValidationError(u"لديك رمز آخر في نفس النشاط.", code="HasOtherCode")

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

            self.code = code

            message = u"تم إدخال الرمز بنجاح."
            message_type = messages.SUCCESS

        else:
            message = u"حصل خطأ ما."
            message_type = messages.ERROR

            print self.fields['string'].errors.as_data()

        return (message_type, message)