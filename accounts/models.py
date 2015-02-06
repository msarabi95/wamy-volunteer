# coding=utf-8
from django.conf import settings
from django.db import models

# Create your models here.
from userena.models import UserenaBaseProfile


class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')

    ar_first_name = models.CharField(u"الاسم الأول", max_length=30)
    ar_middle_name = models.CharField(u"اسم الأب", max_length=30)
    ar_last_name = models.CharField(u"الاسم الأخير", max_length=30)

    en_first_name = models.CharField("First name", max_length=30)
    en_middle_name = models.CharField("Middle name", max_length=30)
    en_last_name = models.CharField("Last name", max_length=30)

    # Special information
    mobile = models.CharField(u"رقم الجوال", max_length=30)
    state = models.ForeignKey("State", related_name="user_profiles", verbose_name=u"المنطقة", null=True)
    university = models.CharField(u"الجامعة", max_length=128)  # CharField or ForeignKey?

    ACADEMIC_YEAR_CHOICES = (
        (1, u"السنة الأولى"),
        (2, u"السنة الثانية"),
        (3, u"السنة الثالثة"),
        (4, u"السنة الرابعة"),
        (5, u"السنة الخامسة"),
        (6, u"السنة السادسة"),
        (7, u"سنة الامتياز"),
    )

    academic_year = models.PositiveIntegerField(u"السنة الدراسية", choices=ACADEMIC_YEAR_CHOICES, default=1)
    specialty = models.CharField(u"التخصص", max_length=128)

    def get_ar_full_name(self):
        return "%s %s %s" % (self.ar_first_name, self.ar_middle_name, self.ar_last_name, )

    def get_en_full_name(self):
        return "%s %s %s" % (self.en_first_name, self.en_middle_name, self.en_last_name, )

    def __unicode__(self):
        return u"ملف المستخدم: %s" % self.user.__unicode__()

    class Meta:
        verbose_name = u"ملف مستخدم"
        verbose_name_plural = u"ملفات المستخدمين"


class State(models.Model):
    name = models.CharField(max_length=128, verbose_name=u"الاسم")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"منطقة"
        verbose_name_plural = u"المناطق"