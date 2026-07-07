from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the custom User model.
    Provides a customized admin interface for managing users
    authenticated by email instead of username, including
    custom fieldsets, search, filtering, and list display.
    """

    model = User
    list_display = ['first_name', 'last_name',
                    'email', 'is_superuser', 'is_active', 'is_staff']
    list_filter = ['is_superuser', 'is_active', 'is_staff']
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = (
        'created_at',
        'updated_at',
        'last_login',
    )
    fieldsets = (
        ('Authentication', {
            'fields': ('email', 'password')
        }),
        ("Personal info", {
            "fields": ("first_name", "last_name"),
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser')
        }),
        ('Group Permissions', {
            'fields': ('groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'created_at', 'updated_at')
        })
    )
    add_fieldsets = (
        (
            'New User',
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'first_name',
                    'last_name',
                    'is_staff',
                    'is_active',
                    'is_superuser',
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
