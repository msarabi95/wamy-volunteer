from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Sum
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from codes.forms import RedeemCodeForm
from teams.forms import EvaluationForm


@login_required
def redeem(request):
    """
    GET: show the code submission form.
    POST: submit a code.
    """
    if request.method == "POST":
        form = RedeemCodeForm(request.user, request.POST)
        eval_form = EvaluationForm(request.POST)
        if form.is_valid() and eval_form.is_valid():
            result = form.process()
            messages.add_message(request, *result)
            eval_form.save(form.code.event, request.user)
            return HttpResponseRedirect(reverse("codes:redeem"))
    else:
        code = request.GET.get("code")
        form = RedeemCodeForm(request.user, initial={'string': code})
        eval_form = EvaluationForm()
    return render(request, "codes/redeem.html", {"form": form, "eval_form": eval_form})


@login_required
def report(request):
    """
    Show a summary report for the user's code submissions.
    """
    user = request.user
    credit_sum = user.redeemed_codes.aggregate(sum=Sum("category__credit"))["sum"]
    return render(request, "codes/report.html", {"user": user, "credit_sum": credit_sum})