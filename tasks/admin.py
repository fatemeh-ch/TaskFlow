from django.contrib import admin

from tasks.models import Task, Category

# Register your models here.


class CustomTaskAdmin(admin.ModelAdmin):
    """
        Admin configuration for managing task objects.
    """

    list_display = ['short_title', 'user',
                    'category', 'status', 'priority']
    fields = ('user',
              ('title', 'category'),
              'description',
              ('status', 'priority'),
              ('deadline', 'completed_at'),
              'is_important',
              )
    list_filter = ('category', 'status', 'priority')
    ordering = ('-created_at',)
    search_fields = ('title', 'user__email',)
    readonly_fields = (
        'created_at',
        'updated_at',
    )

    @admin.display(description='Title')
    def short_title(self, obj):
        if len(obj.title) > 30:
            return obj.title[:30] + "..."
        return obj.title


class CategoryAdmin(admin.ModelAdmin):
    """
        Admin configuration for managing task categories.
    """

    fields = ['title', 'slug', 'icon']
    list_display = ['title', 'slug', 'icon']
    ordering = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {
        'slug': ('title',)
    }
    readonly_fields = (
        'created_at',
        'updated_at',
    )


admin.site.register(Task, CustomTaskAdmin)
admin.site.register(Category, CategoryAdmin)