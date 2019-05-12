from django.urls import path
# from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<videoid>/<date>/<object>/<color>/<direction>/<weather>/<lati>/<longi>/',views.detail),
    path('androidRegister/', views.androidRegister),
    path('androidLogin/', views.androidLogin),
    path('userLogin/', views.userLogin),
    path('userLogout/', views.userLogout),
    path('search/<date>/<object>/<color>/<direction>/<weather>/<lati>/<longi>/', views.search),
]