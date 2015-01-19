# coding=utf-8
from django.core.urlresolvers import reverse
from django.db import models


class Team(models.Model):
    name = models.CharField(u"الاسم", max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"فريق"
        verbose_name_plural = u"الفرق"


class Event(models.Model):
    name = models.CharField(u"الاسم", max_length=128)
    team = models.ForeignKey(Team, related_name="events", verbose_name=u"الفريق")
    # allow_multiple = models.BooleanField(default=False)  # allow multiple codes to be submitted per user per event

    def admin_links(self):
        # TODO: the link might need some styling to have a more interesting look?
        kw = {"args": (self.id,)}
        links = [
            (u"أنشئ رموزًا", reverse("admin:create_codes", args=(self.pk, ))),
            (u"استعرض رموز هذا النشاط", ""),  # TODO: add proper reverse statement here
        ]
        for i, (text, url) in enumerate(links):
            links[i] = "<a href='%s'>%s</a>" % (url, text)
        return "<br>".join(links)
    admin_links.allow_tags = True
    admin_links.short_description = ""

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"نشاط"
        verbose_name_plural = u"الأنشطة"