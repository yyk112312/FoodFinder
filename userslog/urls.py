from django.urls import path
from django.contrib.auth import views as auth_views
from userslog import views

app_name = "user"

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.signup_view, name='signup')
    ]