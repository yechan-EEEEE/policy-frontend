from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # Thread
    path('threads/', views.thread_list, name='thread_list'),
    path('threads/<int:thread_pk>/', views.thread_detail, name='thread_detail'),
    path('threads/<int:thread_pk>/like/', views.thread_like, name='thread_like'),

    # Policy별 Thread
    path(
        'policies/<str:plcyNo>/threads/',
        views.thread_list_by_policy,
        name='thread_list_by_policy'
    ),

    # Comment (Thread 기준)
    path(
        'threads/<int:thread_pk>/comments/',
        views.comment_list,
        name='comment_list'
    ),
    path('comments/<int:comment_pk>/', views.comment_detail),
    path('comments/<int:comment_pk>/like/', views.comment_like),
]
