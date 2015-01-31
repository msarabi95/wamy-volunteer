# coding=utf-8
from django.conf import settings
from django.db import models

# Create your models here.
from userena.models import UserenaBaseProfile


class UserProfile(UserenaBaseProfile):
    # FIXME: Shouldn't be `blank=True`
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')

    ar_first_name = models.CharField(u"الاسم الأول", max_length=30, blank=True)
    ar_middle_name = models.CharField(u"اسم الأب", max_length=30, blank=True)
    ar_last_name = models.CharField(u"الاسم الأخير", max_length=30, blank=True)

    en_first_name = models.CharField("First name", max_length=30, blank=True)
    en_middle_name = models.CharField("Middle name", max_length=30, blank=True)
    en_last_name = models.CharField("Last name", max_length=30, blank=True)

    # Special information
    mobile = models.CharField(u"رقم الجوال", max_length=30, blank=True)
    university = models.CharField(u"الجامعة", max_length=128, blank=True)  # CharField or ForeignKey?

    ACADEMIC_YEAR_CHOICES = (
        (1, u"السنة الأولى"),
        (2, u"السنة الثانية"),
        (3, u"السنة الثالثة"),
        (4, u"السنة الرابعة"),
        (5, u"السنة الخامسة"),
        (6, u"السنة السادسة"),
        (7, u"سنة الامتياز"),
    )

    academic_year = models.PositiveIntegerField(u"السنة الدراسية", choices=ACADEMIC_YEAR_CHOICES, default=1, blank=True)
    specialty = models.CharField(u"التخصص", max_length=128, blank=True)

    def get_ar_full_name(self):
        return "%s %s %s" % (self.ar_first_name, self.ar_middle_name, self.ar_last_name, )

    def get_en_full_name(self):
        return "%s %s %s" % (self.en_first_name, self.en_middle_name, self.en_last_name, )

    def __unicode__(self):
        return u"ملف المستخدم: %s" % self.user.__unicode__()

    class Meta:
        verbose_name = u"ملف مستخدم"
        verbose_name_plural = u"ملفات المستخدمين"