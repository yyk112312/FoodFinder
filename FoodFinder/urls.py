"""FoodFinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from FoodFinder import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_app/', include("main_app.urls")),
    path('user/', include("users.urls")),
    url(r'^$', views.Mainview.as_view(), name='main'),
    url(r'about/', views.Aboutview.as_view(), name='about'),
    path('exercise/', include('exercise.urls')),
    path('maps/', include('maps.urls')),
    path('foodlist/', include('foodboard.urls')),
    path('imagecla/', include('imagecla.urls')),
    path('photo/', include('photo.urls')),
    path('check/', include('check.urls'))

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)