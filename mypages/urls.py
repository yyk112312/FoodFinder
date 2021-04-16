from django.urls import path
from . import views

app_name = 'mypages'

urlpatterns = [
    path('mypage/', views.profile_view, name='mypage'),
    path('update/', views.update, name='update'),
    path('password/', views.password_edit_view, name='change_password'),
    path('delete/', views.delete, name='delete')
]