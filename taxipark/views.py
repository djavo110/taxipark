from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages

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
    
class ReviewCreateView(CreateView):
    model = DriverReviews
    form_class = ReviewForm
    template_name = 'add_review.html'
    success_url = reverse_lazy('review_list')
    
class ReviewListView(ListView):
    model = Review
    template_name = 'review_list.html'
    context_object_name = 'reviews'
    def get_queryset(self):
        return super().get_queryset().select_related('driver', 'customer')
    
    
class DealListView(ListView):
    model = Deal    
    template_name = 'deal_list.html' 
    context_object_name = 'deals'
    def get_queryset(self):
        return Deal.objects.select_related('customer', 'car').all()
    

class DealCreateView(CreateView):
    model  = Deal
    form_class = DealForm
    template_name = 'deal_form.html'
    success_url = reverse_lazy('deal_list')

    def form_valid(self, form):
        user_email = self.request.POST.get('email')
        try:
            user = Users.objects.get(email=user_email)
        except Users.DoesNotExist:
            messages.error(self.request, "Bunday foydalanuvchi topilmadi.")
            return redirect('deal_list')

        if form.is_valid():
            deal = form.save(commit=False)
            deal.customer = user
            deal.save()
            return redirect('pay_for_ride', deal_id=deal.id)
        else:
            return self.form_invalid(form)



# @login_required
def mark_arrived(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id, driver=request.user)
    deal.status = 'arrived'
    deal.save()
    return redirect('deal_detail', deal_id=deal.id)

# @login_required
def pay_for_ride(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id, customer=request.user)

    if deal.status != 'arrived':
        return HttpResponse("🚫 Siz hali manzilga yetib bormagansiz!")

    # Balansdan yechish (agar bor bo‘lsa)
    if request.user.balance < deal.price:
        return HttpResponse("❌ Mablag' yetarli emas!")

    request.user.balance -= deal.price
    request.user.save()

    deal.status = 'paid'
    deal.save()

    return redirect('deal_detail', deal_id=deal.id)

class UserCreateView(CreateView):
    model  = Users
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('users')

class CarCreateView(CreateView):
    model = Cars
    form_class = CarForm
    template_name = 'add_car.html'
    success_url = reverse_lazy('car_list')