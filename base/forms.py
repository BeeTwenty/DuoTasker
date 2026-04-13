from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','category',]  # Ensure 'category' is included
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class SetupForm(UserCreationForm):
    LANGUAGE_CHOICES = [
        ('en', _('English')),
        ('nb', _('Norwegian Bokmal')),
    ]

    TIMEZONE_CHOICES = [
        ('UTC', 'UTC'),
        ('Europe/Oslo', 'Europe/Oslo'),
        ('Europe/Stockholm', 'Europe/Stockholm'),
        ('Europe/Copenhagen', 'Europe/Copenhagen'),
        ('Europe/London', 'Europe/London'),
        ('America/New_York', 'America/New_York'),
    ]

    email = forms.EmailField(required=True)
    default_language = forms.ChoiceField(choices=LANGUAGE_CHOICES, initial='en')
    default_timezone = forms.ChoiceField(choices=TIMEZONE_CHOICES, initial='UTC')
    add_predefined_categories = forms.BooleanField(required=False, initial=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
