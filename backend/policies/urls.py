from django.urls import path
from . import views

app_name = 'policies'

urlpatterns = [
    path('chatbot/', views.policy_chatbot, name='policy_chatbot'),
    path('list/', views.policy_list, name='policy_list'),
    path('recommend/ai/', views.policy_recommend, name='policy_recommend'),
    path('fetch/data/', views.fetch_policies, name='fetch_policies'),
    
    path('<str:plcyNo>/', views.policy_detail, name='policy_detail'),
    path('<str:plcyNo>/like/', views.policy_like, name='policy_like'),
    path('<str:plcyNo>/summarize/', views.policy_summarize, name='policy_summarize'),
]
