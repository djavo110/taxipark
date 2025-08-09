from django.db import models

class Users(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    email = models.EmailField(max_length=100, unique=True)
    is_admin = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name
    
class Cars(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),      
        ('on_route', 'On Route'),         
        ('inactive', 'Inactive'),         
        ('broken', 'Broken'),             
    ]
    model = models.CharField(max_length=100)
    number_plate = models.CharField(max_length=15, unique=True)
    color = models.CharField(max_length=30)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='cars')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.model} - {self.number_plate}"
    
class DriverReviews(models.Model):
    driver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='customer_reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.driver.full_name} - {self.rating}"
    
class Payments(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    is_successful = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.amount} on {self.payment_date.strftime('%Y-%m-%d')}"
    
    
class Deal(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),          # Shartnoma tuzilgan
        ('arrived', 'Arrived'),        # Haydovchi yetib kelgan
        ('paid', 'Paid'),              # To‘lov qilingan
        ('cancelled', 'Cancelled'),    # Bekor qilingan
    ]
    customer = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='deals_as_customer')
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='deals')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.customer.full_name} - {self.car.model} ({self.status})"


class Review(models.Model):
    customer = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name='reviews_by_customer'
    )
    driver = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name='reviews_about_driver'
    )
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.customer.full_name} for {self.driver.full_name} - Rating: {self.rating}"
