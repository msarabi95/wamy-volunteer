# coding=utf-8
import random
import string
from django.conf import settings
from django.core.urlresolvers import reverse
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


class Order(models.Model):
    """
    An 'order' that groups sets of codes created together.
    """
    event = models.ForeignKey(Event, related_name="code_orders", verbose_name=u"النشاط")
    date_created = models.DateTimeField(u"تاريخ الإنشاء", auto_now_add=True)

    def description(self):
        contents = [
            (category.name, self.codes.filter(category=category).count()) for category in Category.objects.all()
        ]
        return "<br>".join(u"%s: %s" % item for item in contents)
    description.allow_tags = True
    description.short_description = u"الوصف"

    def admin_links(self):
        if self.id:
            kw = {"args": (self.id, )}

            # Construct the filter url (which will show the codes of a certain order)
            bits = (self._meta.app_label, Code.__name__.lower())
            changelist_url = reverse("admin:%s_%s_changelist" % bits)
            filter_url = "%s?order__id__exact=%s" % (changelist_url, self.id)

            links = [
                (u"حمل كوبونات", reverse("admin:download_coupons", **kw)),
                (u"حمل روابط قصيرة", reverse("admin:download_links", **kw)),
                (u"استعرض رموز هذا الطلب", filter_url),
            ]
            for i, (text, url) in enumerate(links):
                links[i] = "<a href='%s'>%s</a>" % (url, text)
            return "<br>".join(links)
        else:
            return ""
    admin_links.allow_tags = True
    admin_links.short_description = ""

    def is_downloaded(self):
        """
        Return whether all (True), some (None), or none (False) of the codes in this order have been downloaded.
        """
        # Count the undownloaded codes in this order
        undownloaded_count = self.codes.filter(date_downloaded__isnull=True).count()
        if undownloaded_count == 0:
            # If that's equal to 0, then everything has been downloaded
            return True
        elif undownloaded_count == self.codes.count():
            # If that's equal to the number of codes within the order, then nothing has been downloaded
            return False
        else:
            # Other than that, it could be that the order was partially downloaded
            return None
    is_downloaded.boolean = True
    is_downloaded.short_description = u"تم تحميله؟"

    def __unicode__(self):
        return "%s - %s" % (self.event.name, str(self.date_created))

    class Meta:
        verbose_name = u"طلب"
        verbose_name_plural = u"الطلبات"


class Code(models.Model):
    category = models.ForeignKey(Category, related_name="codes", verbose_name=u"الفئة")
    event = models.ForeignKey(Event, related_name="codes", verbose_name=u"النشاط")
    order = models.ForeignKey(Order, related_name="codes", verbose_name=u"الطلب")
    string = models.CharField(u"النص", unique=True, max_length=CODE_STRING_LENGTH)
    date_created = models.DateTimeField(u"تاريخ الإنشاء", auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="redeemed_codes", null=True, blank=True,
                             verbose_name=u"المستخدم")
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

    def get_credit(self):
        return self.category.credit
    get_credit.short_description = u"عدد الساعات"

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
