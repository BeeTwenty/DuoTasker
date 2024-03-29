from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100)
    is_important = models.BooleanField(default=False)
    is_uncategorized = models.BooleanField(default=False, help_text="Mark as the special 'Uncategorized' category")
    keywords = models.TextField(blank=True, null=True, help_text='Comma separated list of keywords to match for this category')
    

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-is_important', 'name']
    


class Task(models.Model):
    title = models.CharField(max_length=200)
    id = models.BigAutoField(primary_key=True)
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks', null=True)
    

    def __str__(self):
        return self.title
    
