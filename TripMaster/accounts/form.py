from django.forms import ModelForm
from .models import *

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreateCustomer(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class addProduts(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'