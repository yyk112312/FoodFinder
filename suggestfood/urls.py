from django.urls import path
from . import views

app_name ='suggestfood'
urlpatterns = [
    path('suggestfood/',views.export, name="suggestfood"),
    path('suggest/',views.recomomandlist, name='suggest')
]