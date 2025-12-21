from django.urls import path
from . import views

app_name = 'policies'

urlpatterns = [
    path('list/', views.policy_list, name='policy_list'),
    path('<str:plcyNo>/', views.policy_detail, name='policy_detail'),
    path('<str:plcyNo>/like/', views.policy_like, name='policy_like'),
    path('recommend/ai/', views.policy_recommend, name='policy_recommend'),
    path('fetch/data/', views.fetch_policies, name='fetch_policies'),
]
