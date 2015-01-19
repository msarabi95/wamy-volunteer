# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib import admin, messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from codes.admin import CodeAdmin
from codes.forms import CreateCodeForm
from codes.models import Code, Order
from teams.models import Team, Event


class OrderTabularInline(admin.TabularInline):
    model = Order
    readonly_fields = ("description", "date_created", "is_downloaded", "admin_links", )
    extra = 0

    def has_add_permission(self, request):
        """
        Prevent addition of orders manually.
        """
        return False


class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "team", "admin_links")
    search_fields = ("name", "team__name")
    inlines = (OrderTabularInline, )

    def get_urls(self):
        """
        Add the create codes view to urls.
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
        event = get_object_or_404(Event, pk=event_id)

        if request.method == "POST":
            form = CreateCodeForm(event, request.POST)
            if form.is_valid():
                form.create_codes()

                messages.success(request, u"تم إنشاء الرموز المطلوبة.")

                bits = (self.model._meta.app_label, self.model.__name__.lower())
                change_url = reverse("admin:%s_%s_change" % bits, args=(event_id,))
                return HttpResponseRedirect(change_url)
        else:
            form = CreateCodeForm(event)

        context = {"form": form, "opts": event._meta,
                   "original": event,
                   "title": u"أنشئ رموزًا"}
        return render(request, "admin/teams/event/codes.html", context)

admin.site.register(Team)
admin.site.register(Event, EventAdmin)