from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import DealForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

class IndexView(ListView):
    model = Users
    template_name = 'index.html'
    context_object_name = 'users'
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class UserListView(ListView):
    model = Users
    template_name = 'user_list.html'
    context_object_name = 'users'
    def get_queryset(self):
        return super().get_queryset().prefetch_related('cars')

class UserDetailView(DetailView):
    model = Users
    template_name = 'user_detail.html'
    context_object_name = 'user'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = self.object.cars.all()
        context['reviews'] = self.object.reviews.all()
        context['payments'] = self.object.payments.all()
        return context
    
class CarListView(ListView):
    model = Cars
    template_name = 'car_list.html'
    context_object_name = 'cars'
    def get_queryset(self):
        return super().get_queryset().select_related('owner')
    
class PaymentListView(ListView):
    model = Payments
    template_name = 'payment_list.html'
    context_object_name = 'payments'
    def get_queryset(self):
        return super().get_queryset().select_related('user')
    
class ReviewListView(ListView):
    model = DriverReviews
    template_name = 'review_list.html'
    context_object_name = 'reviews'
    def get_queryset(self):
        return super().get_queryset().select_related('driver', 'customer')
    

class DealCreateView(CreateView):
    model  = Deal
    form_class = DealForm
    template_name = 'deal_form.html'
    success_url = reverse_lazy('deal-list')