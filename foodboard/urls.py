from django.conf.urls import url
from foodboard import views
app_name = 'foodboard'

urlpatterns = [
        url(r'^$', views.FoodList.as_view(), name='food_list'),
        url(r'^detail/(?P<pk>\d+)$', views.fooddetail.as_view(), name='foodboard_detail'),
        url('result/', views.searchresult, name='results')
    ]