from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='products'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
]