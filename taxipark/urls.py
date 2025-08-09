from django.urls import path
from .import views
from .views import (
    IndexView,
    UserListView, UserDetailView,
    CarListView,ReviewListView,
    PaymentListView,  UserCreateView,
    DealListView, ReviewCreateView, CarCreateView,
    mark_arrived, pay_for_ride,
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('users/', UserListView.as_view(), name='users'),
    path('user_create/', UserCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('car_create/', CarCreateView.as_view(), name = 'car_create'),
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('add_review/', ReviewCreateView.as_view(), name='add_review'),
    path('payment/', PaymentListView.as_view(), name='payment-list'),
    path('deals/<int:deal_id>/arrived/', mark_arrived, name='mark_arrived'),
    path('deals/<int:deal_id>/pay/', pay_for_ride, name='pay_for_ride'),
    path('deals/', DealListView.as_view(), name='deal_list'),
    path('deals_create/', views.deal_create, name='deal_create'),

]


