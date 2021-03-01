from django.db import models
from .category import Category

# Create your models here.


class StoreInfo(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=50)
    store_image = models.ImageField(upload_to='store/upload')