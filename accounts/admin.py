# coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Sum
from userena.admin import UserenaAdmin
from accounts.models import UserProfile, State


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class CustomUserAdmin(UserenaAdmin):
    inlines = (UserProfileInline, )
    readonly_fields = ('get_credit_sum', )
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff', 'is_active', 'date_joined', 'get_credit_sum')

    def get_queryset(self, request):
        qs = super(CustomUserAdmin, self).get_queryset(request)
        return qs.annotate(credit_sum=Sum('redeemed_codes__category__credit'))

    def get_credit_sum(self, obj):
        return obj.redeemed_codes.aggregate(code_sum=Sum("category__credit"))['code_sum']
    get_credit_sum.short_description = u"مجموع الساعات"
    get_credit_sum.admin_order_field = 'credit_sum'

admin.site.unregister(UserProfile)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(State)