from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:post_pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_pk>/like/', views.post_like, name='post_like'),
    
    path('posts/<int:post_pk>/comments/', views.comment_list, name='comment_list'),
    path('comments/<int:comment_pk>/', views.comment_detail, name='comment_detail'),
    path('comments/<int:comment_pk>/like/', views.comment_like, name='comment_like'),
]
