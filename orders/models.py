from django.db import models
from store.models.product import Product
# Create your models here.

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    postal_code = models.IntegerField()
    city = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    status_choices = (('Processing', 'Processing'),('Prepared','Prepared'),('Waiting Pickup','Waiting Pickup'),('Picked Up', 'Picked Up'), ('In Transit', 'In Transit'), 
                    ('Delivered', 'Delivered'))
    status = models.CharField(max_length=20,choices=status_choices,default='Processing')
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return f'Order {self.id}'
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items', on_delete= models.CASCADE)
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.id)
    def get_cost(self):
        return self.price * self.quantity
