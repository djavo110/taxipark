from django.urls import path
from .views import (
    IndexView,
    UserListView, UserDetailView,
    CarListView,ReviewListView,
    PaymentListView, DealCreateView
    
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('payment/', PaymentListView.as_view(), name='payment-list'),
    path('deal_create/', DealCreateView.as_view(), name='deal_create'),
]


