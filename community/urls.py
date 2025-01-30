# community/urls.py

from django.urls import path
from .views import (
    CommunityListView,
    PostDetailView,
    post_create,
    post_edit,
    post_delete,
    add_comment,
    comment_edit,
    comment_delete
)

app_name = 'community'  # Add this line

urlpatterns = [
    path('', CommunityListView.as_view(), name='community'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', post_create, name='post_create'),
    path('post/<int:pk>/edit/', post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', post_delete, name='post_delete'),
    path('post/<int:post_pk>/comment/add/', add_comment, name='add_comment'),
    path('post/<int:post_pk>/comment/<int:comment_pk>/edit/', comment_edit, name='comment_edit'),
    path('post/<int:post_pk>/comment/<int:comment_pk>/delete/', comment_delete, name='comment_delete'),
]
