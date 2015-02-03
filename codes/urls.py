from django.conf.urls import patterns, url
from django.shortcuts import render

from codes import views

urlpatterns = patterns('',
    url(r'^redeem/', views.redeem, name="redeem"),
    url(r'^report/', views.report, name="report"),
    url(r'^$', lambda request: render(request, "home.html"), name="home"),
)
