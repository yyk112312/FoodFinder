from django.urls import path
from imagecla import views

app_name ='imagecla'

urlpatterns = [
    path('analimg/', views.Deeplearn),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('image/',views.handle_uploaded_file, name='image')
]