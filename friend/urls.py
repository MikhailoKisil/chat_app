from django.urls import path

from . import views

app_name = 'friend'

urlpatterns = [
    path("search/", views.search_friend, name="search_friend"),
    path("add/<slug:nickname>/", views.add_friend, name="add_friend"),
]
