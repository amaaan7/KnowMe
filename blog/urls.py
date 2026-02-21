from django.urls import path, include
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    UserPostListView, AnnouncementListView, AnnouncementDetailView, AnnouncementCreateView,
    EventListView, EventDetailView, EventCreateView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    # Announcements
    path('announcements/', AnnouncementListView.as_view(), name='announcements'),
    path('announcement/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('announcement/new/', AnnouncementCreateView.as_view(), name='announcement-create'),
    # Calendar/Events
    path('calendar/', EventListView.as_view(), name='calendar'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('event/new/', EventCreateView.as_view(), name='event-create'),
    # Info page
    path('info/', views.info, name='info'),
    # Like functionality
    path("post/<int:post_id>/like/", views.toggle_like, name='toggle_like'),
    path("post/<int:post_id>/likes/", views.like_history, name='like_history'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add-comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete-comment'),
    path('post/<int:post_id>/delete-ajax/', views.delete_post_ajax, name='delete-post-ajax'),
    path('api/posts/', views.api_posts),
    path('api/', include('api.urls')),
]
