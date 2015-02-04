# coding=utf-8
from django import forms
from django.db import IntegrityError
from teams.models import EvaluationCriterion, CriterionResponse, Evaluation


class EvaluationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        """
        Dynamically add a field for each evaluation criterion.
        """
        super(EvaluationForm, self).__init__(*args, **kwargs)

        for criterion in EvaluationCriterion.objects.all():
            label = u"%s (من 1 إلى %s)" % (criterion.description, criterion.max_score)
            self.fields['criterion_%s' % criterion.pk] = forms.IntegerField(label=label,
                                                                            min_value=1, max_value=criterion.max_score)
            # self.fields['criterion_%s' % criterion.pk].widget.attrs = {"class": "form-control"}

    def save(self, event, user, *args, **kwargs):
        """
        Save a CriterionResponse object for each criterion.
        """
        evaluation = Evaluation.objects.create(event=event, user=user)

        def get_criterion(str):
            return EvaluationCriterion.objects.get(pk=int(str.split("_")[1]))

        for field in self.fields:
            CriterionResponse.objects.create(evaluation=evaluation, criterion=get_criterion(field),
                                             response=self.cleaned_data[field])