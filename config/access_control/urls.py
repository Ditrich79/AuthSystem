from django.urls import path
from . import views


urlpatterns = [
    path('access_rules/', views.AccessRuleListView.as_view(), name='access-rules-list'),
    path('access_rules/<int:pk>/', views.AccessRuleDetailView.as_view(), name='access-rules-detail'),
]