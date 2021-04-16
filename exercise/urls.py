from django.conf.urls import url
from django.urls import path
from exercise import views

app_name='exercise'

urlpatterns = [
    url(r'^$', views.exerciseList.as_view(), name='exercise_list'),
    url(r'^detail/(?P<pk>\d+)$', views.exerciseDetail.as_view(), name='exercise_detail'),
]