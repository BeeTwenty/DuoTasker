from django.contrib import admin
from .models import Category, Task

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'is_important', 'is_uncategorized')
    search_fields = ('name',)
    list_filter = ('is_important', 'is_uncategorized')
    fields = ('name', 'icon', 'is_important', 'keywords', 'is_uncategorized')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'completed')
    search_fields = ('title',)
    list_filter = ('completed', 'category')
