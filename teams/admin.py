from django.conf.urls import patterns, url
from django.contrib import admin
from django.shortcuts import render
from teams.models import Team, Event



class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "team", "admin_links")

    # TODO: create codes view and url
    def get_urls(self):
        """
        Add the entries view to urls.
        """
        urls = super(EventAdmin, self).get_urls()
        extra_urls = patterns("",
            url("^(?P<event_id>\d+)/codes/$",
                self.admin_site.admin_view(self.create_codes),
                name="create_codes"),
        )
        return extra_urls + urls

    def create_codes(self, request, event_id):
        """
        GET: show the code creation form.
        POST: create codes according to what's posted.
        """
        return render(request, "admin/teams/event/codes.html")


admin.site.register(Team)
admin.site.register(Event, EventAdmin)