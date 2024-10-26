"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
#python manage.py runserver
from django.contrib import admin
from django.urls import path

from task.views import welcome, regist_user, get_list_user, get_list_game, get_game, get_user, check_rating_entry, \
    rating_finish, check_feedback_entry, feedback_finish

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome),
    path('regist_user/', regist_user),
    path('users_list/', get_list_user),
    path('list_game/', get_list_game),
    path('list_game/<int:game_id>/', get_game),
    path('list_user/<int:user_id>/', get_user),
    path('check_rating_entry/', check_rating_entry),
    path('check_rating_entry/rating/', rating_finish),
    path('check_feedback_entry/', check_feedback_entry),
    path('check_feedback_entry/feedback/', feedback_finish),
]

