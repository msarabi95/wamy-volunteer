from django.contrib import admin
from django.conf.urls import url, patterns
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from codes.models import Category, Code, Order


class CodeAdmin(admin.ModelAdmin):
    list_display = ("string", "event", "category", "is_downloaded", "is_redeemed", "user")
    readonly_fields = ("string", )
    search_fields = ("string", "event__name", "user__username")
    list_filter = ("category__name",)

    def has_add_permission(self, request):
        """
        Prevent addition of codes manually.
        """
        return False


class OrderAdmin(admin.ModelAdmin):
    list_display = ("description",  "date_created", "event", "is_downloaded", "admin_links", )
    readonly_fields = ("description",  "date_created", "event", "is_downloaded", "admin_links", )
    search_fields = ("event", )

    COUPON = "coupon"
    LINK = "link"

    DOWNLOAD_TYPES = (
        COUPON,
        LINK,
    )

    def has_add_permission(self, request):
        """
        Prevent addition of orders manually.
        """
        return False

    def get_urls(self):
        """
        Add the download view to the urls.
        """
        urls = super(OrderAdmin, self).get_urls()
        extra_urls = patterns("",
            url("^(?P<order_id>\d+)/download/coupons/$",
                self.admin_site.admin_view(self.download_order),
                {"download_type": self.COUPON},
                name="download_coupons"),
            url("^(?P<order_id>\d+)/download/links/$",
                self.admin_site.admin_view(self.download_order),
                {"download_type": self.LINK},
                name="download_links"),
        )
        return extra_urls + urls

    def download_order(self, request, order_id, download_type):
        """
        Download the passed order as coupons or short links.
        """
        order = get_object_or_404(Order, pk=order_id)

        # TODO: implement downloading

        # Mark codes as downloaded
        order.codes.update(date_downloaded=timezone.now())

        return HttpResponse("HELLO")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "credit")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Code, CodeAdmin)
