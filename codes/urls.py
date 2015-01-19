from django.conf.urls import patterns, url

from codes import views

urlpatterns = patterns('',
    url(r'^redeem/', views.redeem, name="redeem"),
    url(r'^report/', views.report, name="report"),
)
