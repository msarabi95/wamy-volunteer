# coding=utf-8
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Team(models.Model):
    name = models.CharField(u"الاسم", max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"فريق"
        verbose_name_plural = u"الفرق"


class Event(models.Model):
    name = models.CharField(u"الاسم", max_length=128)
    team = models.ForeignKey(Team, related_name="events", verbose_name=u"الفريق")
    date_created = models.DateTimeField(auto_now_add=True)
    # allow_multiple = models.BooleanField(default=False)  # allow multiple codes to be submitted per user per event

    def admin_links(self):
        # TODO: the link might need some styling to have a more interesting look?
        kw = {"args": (self.id,)}

        from codes.models import Code

        # Construct the filter url (which will show the codes of a certain order)
        bits = (Code._meta.app_label, Code.__name__.lower())
        changelist_url = reverse("admin:%s_%s_changelist" % bits)
        filter_url = "%s?%s__id__exact=%s" % (changelist_url, self.__class__.__name__.lower(), self.id)

        links = [
            (u"أنشئ رموزًا", reverse("admin:create_codes", args=(self.pk, ))),
            (u"استعرض رموز هذا النشاط", filter_url),
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


class EvaluationCriterion(models.Model):
    label = models.CharField(max_length=128, verbose_name=u"العنوان")
    description = models.CharField(max_length=128, verbose_name=u"الوصف",
                                   help_text=u"السؤال الذي سيظهر لمن سيقوم بالتقييم.")
    max_score = models.PositiveIntegerField(default=5, verbose_name=u"الحد الأقصى",
                                        help_text=u"معيار التقييم عبارة عن سلم من ١ إلى الحد الأقصى الذي يتم تحديده.")

    def __unicode__(self):
        return self.label

    class Meta:
        verbose_name = u"معيار تقييم"
        verbose_name_plural = u"معايير التقييم"


class Evaluation(models.Model):
    event = models.ForeignKey(Event, related_name="evaluations", verbose_name=u"النشاط")
    user = models.ForeignKey(User, related_name="evaluations", verbose_name=u"المستخدم")
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Evaluation of %s by %s" % (self.event.__unicode__(), self.user.__unicode__())

    class Meta:
        unique_together = ("event", "user")
        verbose_name = u"تقييم"
        verbose_name_plural = u"التقييمات"


class CriterionResponse(models.Model):
    evaluation = models.ForeignKey(Evaluation, related_name="criterion_responses")
    criterion = models.ForeignKey(EvaluationCriterion, verbose_name=u"المعيار")
    response = models.PositiveIntegerField(verbose_name=u"التقييم")

    def __unicode__(self):
        return "Response to %s in %s" % (self.criterion.__unicode__(), self.evaluation.__unicode__())

    class Meta:
        verbose_name = u"تقييم فرعي"
        verbose_name_plural = u"التقييمات الفرعية"