# coding=utf-8
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
    team = models.ForeignKey(Team, verbose_name=u"الفريق")
    # allow_multiple = models.BooleanField(default=False)  # allow multiple codes to be submitted per user per event

    def admin_links(self):
        kw = {"args": (self.id,)}
        links = [
            (u"أنشئ رموزًا", ""),
            (u"استعرض رموز هذا النشاط", ""),
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