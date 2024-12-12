from django.urls import path
from accounts.views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), # localhost:8000/auth/register
    path('login/', LoginView.as_view(), name='login'), # localhost:8000/auth/login
]