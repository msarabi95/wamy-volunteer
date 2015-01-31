from django.conf.urls import patterns, include, url

from django.contrib import admin
from accounts.forms import CustomSignupForm

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wamy_volunteer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/signup/$', 'userena.views.signup', {'signup_form': CustomSignupForm}),
    url(r'^accounts/', include('userena.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include("codes.urls", namespace="codes"),)
)
