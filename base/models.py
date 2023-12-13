from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=200)
    id = models.BigAutoField(primary_key=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
