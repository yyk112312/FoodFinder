from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="home"),
    path('plans/',views.plan_category,name="plan_category"),
    path('select-food/',views.select_food,name="select_food"),
    path('update-food-item/<int:id>',views.updatefooditem,name="update_food_item"),
    path('delete-food-item/<int:id>',views.deletefooditem,name="delete_food_item"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)