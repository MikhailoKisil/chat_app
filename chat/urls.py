from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_user, name="register"),
    path("accounts/login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("chat/", views.chat, name="chat"),
    path("chat/<slug:other_username>/", views.room, name="room"),
    path("user_status/<int:user_pk>/", views.user_status, name="user_status")
]