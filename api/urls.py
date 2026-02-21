from django.urls import path
from .views import post_list_api, toggle_like_api

urlpatterns = [
    path('posts/', post_list_api),
    path('posts/<int:post_id>/like/', toggle_like_api),
]