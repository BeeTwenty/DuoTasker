# In forms.py (create this file if it doesn't exist in your app)
from django import forms
from .models import Task, Category

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','category',]  # Ensure 'category' is included
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
