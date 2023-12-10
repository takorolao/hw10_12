from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']
        widgets = {
            'status': forms.Select(choices=Task.STATUS_CHOICES),
        }

class SignUpWithVerificationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']