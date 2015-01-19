from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from codes.forms import RedeemCodeForm


def redeem(request):
    """
    GET: show the code submission form.
    POST: submit a code.
    """
    if request.method == "POST":
        form = RedeemCodeForm(request.user, request.POST)
        if form.is_valid():
            result = form.process()
            messages.add_message(request, *result)
            return HttpResponseRedirect(reverse("codes:redeem"))
    else:
        form = RedeemCodeForm(request.user)
    return render(request, "codes/redeem.html", {"form": form})


def report(request):
    """
    Show a summary report for the user's code submissions.
    """
    pass