# coding=utf-8
from django import forms
from userena.forms import SignupForm
from accounts.models import UserProfile, State


# Adapted from work on Enjaz Portal by Osama Khalid
class CustomSignupForm(SignupForm):
    """
    A form that includes extra signup fields.
    """
    ar_first_name = forms.CharField(label=UserProfile._meta.get_field('ar_first_name').verbose_name,
                                max_length=30)
    ar_middle_name = forms.CharField(label=UserProfile._meta.get_field('ar_middle_name').verbose_name,
                                max_length=30)
    ar_last_name = forms.CharField(label=UserProfile._meta.get_field('ar_last_name').verbose_name,
                                max_length=30)
    en_first_name = forms.CharField(label=UserProfile._meta.get_field('en_first_name').verbose_name,
                                max_length=30)
    en_middle_name = forms.CharField(label=UserProfile._meta.get_field('en_middle_name').verbose_name,
                                max_length=30)
    en_last_name = forms.CharField(label=UserProfile._meta.get_field('en_last_name').verbose_name,
                                max_length=30)

    # Since the mobile number starts with a zero, store it as a string.
    mobile = forms.CharField(label=UserProfile._meta.get_field('mobile').verbose_name, max_length=30)
    state = forms.ChoiceField(label=UserProfile._meta.get_field('state').verbose_name,
                              choices=State.objects.values_list('id', 'name'))
    university = forms.CharField(label="%s (%s)" % (UserProfile._meta.get_field('university').verbose_name,
                                 u"الاسم كاملاً باللغة العربية") )
    academic_year = forms.ChoiceField(label=UserProfile._meta.get_field('academic_year').verbose_name,
                                      choices=UserProfile.ACADEMIC_YEAR_CHOICES)
    specialty = forms.CharField(label=UserProfile._meta.get_field('specialty').verbose_name, max_length=128)

    def clean(self):
        # Call the parent class's clean function.
        cleaned_data = super(CustomSignupForm, self).clean()

        # Remove spaces at the start and end of all text fields.
        for field in cleaned_data:
            if isinstance(cleaned_data[field], unicode):
                cleaned_data[field] = cleaned_data[field].strip()

        # Make sure that the mobile numbers contain only digits and
        # pluses:
        if 'mobile' in cleaned_data:
            mobile_msg = ""
            if len(cleaned_data['mobile']) < 10:
                mobile_msg = u"الرقم الذي أدخلت ناقص"
            for char in cleaned_data['mobile']:
                if not char in '1234567890+':
                    mobile_msg = u"أدخل أرقاما فقط"
                    break
            if mobile_msg:
                self._errors['mobile'] = self.error_class([mobile_msg])
                del cleaned_data['mobile']

        return cleaned_data

    def save(self):
        """
        Override the save method to create a custom profile for the user.
        """
        # All username names should be lower-case.
        self.cleaned_data['username'] = self.cleaned_data['username'].lower()

        # Save the parent form and get the user
        new_user = super(CustomSignupForm, self).save()

        # Remove the profile that's automatically created by Userena
        new_user.profile.delete()

        new_user.profile = UserProfile(
            ar_first_name=self.cleaned_data['ar_first_name'],
            ar_middle_name=self.cleaned_data['ar_middle_name'],
            ar_last_name=self.cleaned_data['ar_last_name'],
            en_first_name=self.cleaned_data['en_first_name'],
            en_middle_name=self.cleaned_data['en_middle_name'],
            en_last_name=self.cleaned_data['en_last_name'],
            mobile=self.cleaned_data['mobile'],
            state=State.objects.get(pk=self.cleaned_data['state']),
            university=self.cleaned_data['university'],
            academic_year=self.cleaned_data['academic_year'],
            specialty=self.cleaned_data['specialty'],
        )

        new_user.profile.save()

        return new_user