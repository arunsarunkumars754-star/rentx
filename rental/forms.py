from django import forms
from .models import CUSTOMERS, VEHICLES, VEHICLE_CATEGORY, BOOKING, REPORT, PAYMENT, RENTAL, CANCELLATION

class CustomerForm(forms.ModelForm):
    class Meta:
        model = CUSTOMERS
        fields = '__all__'

class VehicleForm(forms.ModelForm):
    class Meta:
        model = VEHICLES
        fields = '__all__'
        
class BookingForm(forms.ModelForm):
    class Meta:
        model = BOOKING
        fields = '__all__'
