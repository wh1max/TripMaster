from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    passport_number = models.CharField(max_length=200, null=True)
    passport_date_created = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    SUPPLIER = (
        ('Airlines ', 'Airlines '),
        ('Hotels ', 'Hotels '),
        ('Car rental companies', 'Car rental companies'),
        ('Travel insurance companies', 'Travel insurance companies'),
        ('Tour operators', 'Tour operators'),
    )
    category = (
        ('Voyage Organizer', 'Voyage Organizer'),
        ('Omra', 'Omra'),
        ('Billetterie', 'Billetterie'),
        ('Voyage A La Cart', 'Voyage A La Cart'),
        ('Location Voiture', 'Location Voiture'),
        ('sejour linguistique','sejour linguistique'),
    )
    name = models.CharField(max_length=200, null=True)
    purchased_price = models.FloatField(null=True)
    price = models.FloatField(null=True)
    categories = models.CharField(max_length=200, null=True, choices=category)
    supplier = models.CharField(max_length=200, null=True, choices=SUPPLIER)
    date_purchased = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, related_name="order")
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    total_items = models.IntegerField(default=0)

    def __str__(self):
        return f"Order {self.product} by {self.customer.name}"
    
class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)