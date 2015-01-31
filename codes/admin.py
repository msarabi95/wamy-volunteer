from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, patterns
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
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
        # --- Permission checks ---
        if not request.user.is_authenticated():
            raise PermissionDenied

        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied

        order = get_object_or_404(Order, pk=order_id)
        domain = Site.objects.get_current().domain

        if download_type == self.COUPON:
            endpoint = "http://api.qrserver.com/v1/create-qr-code/?size=180x180&data=" + domain

            response = render(request, 'codes/includes/coupons.html', {"order": order,
                                                                       "domain": domain,
                                                                       "endpoint": endpoint})
        elif download_type == self.LINK:
            endpoint = "https://api-ssl.bitly.com/v3/shorten?format=txt&access_token=%(api_key)s&longUrl=" % {"api_key": settings.BITLY_KEY}

            response = render(request, 'codes/includes/links.html', {"order": order,
                                                                     "domain": domain,
                                                                     "endpoint": endpoint})
        # Mark codes as downloaded
        order.codes.update(date_downloaded=timezone.now())

        return response


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "credit")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Code, CodeAdmin)
