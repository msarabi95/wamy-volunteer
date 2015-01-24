import os
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, patterns
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context
from django.template.loader import get_template
from django.utils import timezone
from codes.models import Category, Code, Order
from xhtml2pdf import pisa


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

        if download_type == self.COUPON:
            # Render html content through html template with context
            template = get_template('codes/includes/coupons.html')
            html = template.render(Context({"order": order}))

            # Write PDF to file
            file = open(os.path.join(settings.MEDIA_ROOT, 'order_%s.pdf' % order.pk), "w+b")
            pisaStatus = pisa.CreatePDF(html, dest=file)

            # Return PDF document through a Django HTTP response
            file.seek(0)
            pdf = file.read()
            file.close()
            os.remove(os.path.join(settings.MEDIA_ROOT, file.name))

            response = HttpResponse(pdf, content_type='application/pdf')

        elif download_type == self.LINK:

            response = HttpResponse("HELLO")

        # Mark codes as downloaded
        order.codes.update(date_downloaded=timezone.now())

        return response


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "credit")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Code, CodeAdmin)
