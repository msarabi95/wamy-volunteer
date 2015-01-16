from django.contrib import admin
from teams.models import Team, Event


class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "team", "admin_links")


admin.site.register(Team)
admin.site.register(Event, EventAdmin)