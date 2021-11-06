from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserDetailView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('user/', UserDetailView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]