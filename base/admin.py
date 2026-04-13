from django.contrib import admin
from .models import Category, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'is_important', 'is_uncategorized')
    search_fields = ('name', 'keywords')
    list_filter = ('is_important', 'is_uncategorized')
    fields = ('name', 'icon', 'is_important', 'keywords', 'is_uncategorized')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'keywords':
            formfield.help_text = (
                'Comma-separated aliases and item names. '
                'Use multiple languages here, for example: milk, melk, brod, brodskive.'
            )
        return formfield


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'completed')
    search_fields = ('title',)
    list_filter = ('completed', 'category')
