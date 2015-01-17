from django.contrib import admin
from codes.models import Category, Code


class CodeAdmin(admin.ModelAdmin):
    list_display = ("string", "is_downloaded", "is_redeemed")
    # TODO: make all fields readonly

admin.site.register(Category)
admin.site.register(Code, CodeAdmin)
