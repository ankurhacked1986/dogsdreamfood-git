from django.db import models
from .category import Category

# Create your models here.


class Product(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)
    description = models.TextField(default='')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    image = models.ImageField(upload_to='product/upload')
    product_image_1 = models.ImageField(upload_to='product/upload')
    is_featured = models.BooleanField(default=False)

    @staticmethod
    def get_all_product():
        return Product.objects.all()
    
    @staticmethod
    def get_product_by_categoryid(categoryid):
        if categoryid:
            return Product.objects.filter(category=categoryid)
        else:
            return Product.get_all_product()
    @staticmethod
    def get_all_featured_products():
        return Product.objects.filter(is_featured=True)