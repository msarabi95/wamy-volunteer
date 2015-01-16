from django.contrib import admin
from django.contrib.auth.models import User
from userena.admin import UserenaAdmin
from accounts.models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class CustomUserAdmin(UserenaAdmin):
    inlines = (UserProfileInline, )


admin.site.unregister(UserProfile)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
