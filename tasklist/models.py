from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
            return self.title
