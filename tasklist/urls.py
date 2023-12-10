from django.urls import path
from .views import task_list, task_detail, create_task, edit_task, user_login, logout_view, SignUpWithVerificationView, register
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', task_list, name='task_list'),
    path('<int:task_id>/', task_detail, name='task_detail'),
    path('create/', create_task, name='create_task'),
    path('<int:task_id>/edit/', edit_task, name='edit_task'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register' ),
    path('logout/', logout_view, name='logout'),
    # path('signup/', SignUpWithVerificationView.as_view(), name='signup_with_verification'),
    # path('email-sent/', email_sent, name='email_sent'),
    # path('email-verification/<int:user_id>/', email_verification, name='email_verification'),
]
