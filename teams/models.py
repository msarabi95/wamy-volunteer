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

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"نشاط"
        verbose_name_plural = u"الأنشطة"