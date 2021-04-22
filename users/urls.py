from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name="register"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('filling-details/<int:id>/',views.details_form,name="filling_details"),
    path('set-target-wt/',views.target_wt,name="set_target_wt"),
    path('calorie-goal/',views.calorie_goal,name="calorie_goal"),
    path('profile/',views.profile,name="profile"),
]
