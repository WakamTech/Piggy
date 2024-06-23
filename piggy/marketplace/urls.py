from django.urls import path
from . import views
from .views import (
    UserListView, UserUpdateView, UserDeleteView, 
    AdListView, AdValidateView, AdDeleteView, 
    OrderListView, OrderUpdateView, OrderDeleteView,
    get_stats, get_configs
)

urlpatterns = [
    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('ads/', views.AdListCreateView.as_view(), name='ad_list_create'),
    path('ads/<int:pk>/', views.AdRetrieveUpdateDestroyView.as_view(), name='ad_detail'),
    path('delivery_fees/', views.DeliveryFeeListCreateView.as_view(), name='delivery_fee_list_create'),
    path('delivery_fees/<int:pk>/', views.DeliveryFeeRetrieveUpdateDestroyView.as_view(), name='delivery_fee_detail'),
    path('butcheries/', views.ButcheryListCreateView.as_view(), name='butchery_list_create'),
    path('butcheries/<int:pk>/', views.ButcheryRetrieveUpdateDestroyView.as_view(), name='butchery_detail'),
    path('orders/', views.OrderListCreateView.as_view(), name='order_list_create'),
    path('orders/<int:pk>/', views.OrderRetrieveUpdateDestroyView.as_view(), name='order_detail'),
    path('notifications/', views.NotificationListCreateView.as_view(), name='notification_list_create'),
    path('notifications/<int:pk>/', views.NotificationRetrieveUpdateDestroyView.as_view(), name='notification_detail'),
    path('reviews/', views.ReviewListCreateView.as_view(), name='review_list_create'),
    path('reviews/<int:pk>/', views.ReviewRetrieveUpdateDestroyView.as_view(), name='review_detail'),
    path('carts/', views.CartListCreateView.as_view(), name='cart_list_create'),
    path('carts/<int:pk>/', views.CartRetrieveUpdateDestroyView.as_view(), name='cart_detail'),
    path('calculate_delivery_fee/', views.calculate_delivery_fee, name='calculate_delivery_fee'),
    path('admin/users/', UserListView.as_view(), name='user-list'),
    path('admin/users/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('admin/users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('admin/ads/', AdListView.as_view(), name='ad-list'),
    path('admin/ads/<int:pk>/validate/', AdValidateView.as_view(), name='ad-validate'),
    path('admin/ads/<int:pk>/delete/', AdDeleteView.as_view(), name='ad-delete'),
    path('admin/orders/', OrderListView.as_view(), name='order-list'),
    path('admin/orders/<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
    path('admin/orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),
    path('admin/stats/', get_stats, name='get-stats'),
    path('api/configs/', get_configs, name='get_configs'),
]