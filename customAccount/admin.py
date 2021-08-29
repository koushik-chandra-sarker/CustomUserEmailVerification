from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from customAccount.forms import UserCreationForm, UserChangeForm
from .models import EmailConfirmed

User = get_user_model()
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_admin']
    list_filter = ['is_admin']
    fieldsets = (
        (
            None, {
                'fields': ('email', 'first_name', 'last_name', 'password')
            }
        ),
        (
            "Permission", {
                'fields': ('is_admin', 'is_staff')
            }
        )
    )
    add_fieldsets = (
        (
            None, {
                'fields': ('email', 'first_name', 'last_name', 'is_active', 'password1', 'password2')
            }
        ),
        (
            "Permission", {
                'fields': ('is_admin', 'is_staff')
            }
        )
    )
    ordering = ['email']
    search_fields = ['email']
    filter_horizontal = ()


@admin.register(EmailConfirmed)
class EmailConfirmedAdmin(BaseUserAdmin):
    list_display = ['user', 'first_name', 'last_name', 'activation_key', 'email_confirm', 'created_at']

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    filter_horizontal = ()
    list_filter = []
    ordering = []
    search_fields = []
