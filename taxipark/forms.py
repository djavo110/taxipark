from django import forms
from .models import *

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = "__all__"

class UserForm(forms.ModelForm):
    class  Meta:
        model = Users
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'

class CarForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = '__all__'