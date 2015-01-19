from django.http import HttpResponse
from django.shortcuts import render


def redeem(request):
    """
    GET: show the code submission form.
    POST: submit a code.
    """
    if request.method == "POST":
        # do so and so
        pass
    return render(request, "codes/redeem.html")


def report(request):
    """
    Show a summary report for the user's code submissions.
    """
    pass