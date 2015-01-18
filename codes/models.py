# coding=utf-8
import random
import string
from django.conf import settings
from django.db import models
from teams.models import Event


CODE_STRING_LENGTH = 16
CODE_STRING_CHARS = string.ascii_uppercase + string.digits


class Category(models.Model):
    name = models.CharField(u"الاسم", max_length=32)
    credit = models.FloatField(u"عدد الساعات")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"فئة"
        verbose_name_plural = u"الفئات"


class Code(models.Model):
    category = models.ForeignKey(Category, verbose_name=u"الفئة")
    event = models.ForeignKey(Event, verbose_name=u"النشاط")
    string = models.CharField(u"النص", unique=True, max_length=CODE_STRING_LENGTH)
    date_created = models.DateTimeField(u"تاريخ الإنشاء", auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=u"المستخدم")
    date_redeemed = models.DateTimeField(null=True, blank=True, verbose_name=u"تاريخ الاستخدام")

    date_downloaded = models.DateTimeField(null=True, blank=True, verbose_name=u"تاريخ التحميل")

    def __init__(self, *args, **kwargs):
        """
        Generate a unique string for the current code.
        """
        super(Code, self).__init__(*args, **kwargs)

        # If the code is new (not being loaded from db), then generate a unique string
        if self.string == "":
            while True:
                random_string = ''.join(random.choice(CODE_STRING_CHARS) for idx in range(CODE_STRING_LENGTH))
                # If the string is unique, then break the loop. Otherwise keep generating random strings.
                if not self.__class__.objects.filter(string=random_string).exists():
                    break
            self.string = random_string

    def is_redeemed(self):
        return self.user is not None
    is_redeemed.boolean = True
    is_redeemed.short_description = u"تم استخدامه؟"

    def is_downloaded(self):
        return self.date_downloaded is not None
    is_downloaded.boolean = True
    is_downloaded.short_description = u"تم تحميله؟"

    def __unicode__(self):
        return self.string

    class Meta:
        verbose_name = u"رمز"
        verbose_name_plural = u"الرموز"