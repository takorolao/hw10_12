from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.views import View as TemplateView, View
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse_lazy
from .forms import SignUpWithVerificationForm
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
import ssl
import smtplib


def task_list(request):
    tasks = Task.objects.all()
    paginator = Paginator(tasks, 5)  # Пагинация по 5 задач на страницу
    page = request.GET.get('page')
    tasks = paginator.get_page(page)
    return render(request, 'tasklist/task_list.html', {'tasks': tasks})

def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasklist/task_detail.html', {'task': task})

# представление для создания новой задачи
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  
            task.save()
            return redirect('task_list')  
        else:
            messages.error(request, form.errors)
    else:
        form = TaskForm()

    return render(request, 'tasklist/create_task.html', {'form': form})

# представление для редактирования существующей задачи
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.save()
        return redirect('task_list')
    return render(request, 'tasklist/edit_task.html', {'task': task})



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматически входим после регистрации
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class SignUpWithVerificationView(CreateView):
    model = User
    template_name = 'registration/signup_with_verification.html'
    form_class = SignUpWithVerificationForm
    success_url = reverse_lazy('task_list')


    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(f'/verify/{user.pk}/{token}/') 
        subject = 'Подтвердите свой адрес электронной почты'
        message = f'Hello {user.username}, please click the link below to verify your email:\n\n{verify_url}'
        connection = smtplib.SMTP('smtp.gmail.com', 587)
        connection.starttls(context=ssl.create_default_context())
        send_mail(subject, message, 'kemelovetaukekhan@gmail.com', [user.email], connection=connection)
        
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user.is_active = False
        user.save()
        self.send_verification_email(self.object)
        return response


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('task_list')