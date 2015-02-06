# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib import admin, messages
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from codes.forms import CreateCodeForm
from codes.models import Code, Order
from teams.models import Team, Event, EvaluationCriterion, CriterionResponse


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

    EVALUATION_COUNT = "evaluation_count"  # the field name

    def get_evaluation_fields(self):
        """
        Return a list of field names for evaluation fields; in the format `criterion_X_avg`, where X
        is the PK of each evaluation criterion, in addition to `evaluation_count` field.
        """
        return tuple(["criterion_%s_avg" % criterion.pk
                      for criterion in EvaluationCriterion.objects.all()] + [self.EVALUATION_COUNT])

    def get_readonly_fields(self, request, obj=None):
        """
        Dynamically add a field for each evaluation criterion to display the average score on that criterion.
        """
        readonly_fields = super(EventAdmin, self).get_readonly_fields(request, obj)
        return readonly_fields + self.get_evaluation_fields()

    def get_list_display(self, request):
        list_display = super(EventAdmin, self).get_list_display(request)
        joined = list(list_display + self.get_evaluation_fields())

        # To make things neater, move `admin_links` field to the end
        joined.append(joined.pop(joined.index("admin_links")))
        return tuple(joined)

    def __getattr__(self, item):
        """
        For evaluation count field, return a callable that returns the evaluation count for an event.
        For evaluation fields, which are dynamically added, return a callable that returns the average
         responses for a certain criterion in a certain event.
        """
        if item == self.EVALUATION_COUNT:
            def func(obj):
                return obj.evaluations.count()
            func.short_description = u"عدد التقييمات"
            return func

        elif item in self.get_evaluation_fields():
            def get_criterion(str):
                return EvaluationCriterion.objects.get(pk=int(str.split("_")[1]))

            def func(obj):
                return CriterionResponse.objects.filter(evaluation__event=obj,
                                                        criterion=get_criterion(item))\
                                                        .aggregate(avg=Avg("response"))["avg"]
            func.short_description = u"معدل تقييم %s" % get_criterion(item).label
            return func

        else:
            raise AttributeError

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
admin.site.register(EvaluationCriterion)