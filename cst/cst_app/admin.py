from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.site_header = 'Google Ads customer portal'

''' UserAdmin class helps to display users details in django admin panel '''

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (_('User credential'), {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'role')}),
        (_('Permissions'), {
            'fields': ('is_linked', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'phone', 'email', 'password1', 'password2')}
        ),
    )

    list_display = ('email', 'first_name', 'last_name', 'phone', 'role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('phone', 'first_name', 'last_name', 'email')
    ordering = ('email',)


class AgencyAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Agency details'), {'fields': ('agency_name', 'created_by', 'agency_url', )}),
        (_('Agency contact'), {'fields': ('address', 'work_phone', )}),
        (_('Permissions'), {
            'fields': ('is_active', ),
        }),
        (_('Important dates'), {'fields': ('created_at', 'updated_at', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('agency_name', 'address', 'work_phone', 'created_by','is_active',)}
        ),
    )
    readonly_fields = ('created_at', 'updated_at', ) 

    list_display = ('agency_name', 'agency_url', 'created_by', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_by')
    search_fields = ('agency_name', 'created_by', 'last_name', 'email')
    ordering = ('agency_name',)

admin.site.register(Agency, AgencyAdmin)

class CustomerAdmin(BaseUserAdmin):
    fieldsets = (
        (_('User credential'), {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'role')}),
        (_('Permissions'), {
            'fields': ('is_linked', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'phone', 'email', 'password1', 'password2')}
        ),
    )

    list_display = ('email', 'first_name', 'last_name', 'phone', 'role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('phone', 'first_name', 'last_name', 'email')
    ordering = ('email',)

admin.site.register(Customer, CustomerAdmin)