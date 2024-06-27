from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('get_news', views.get_news, name='get_news'),
    path('get_saved_news', views.get_saved_news, name='get_saved_news'),
    path('save_news', views.save_news, name='save_news'),
    path('like_open', views.like_open, name='like_open'),
]
