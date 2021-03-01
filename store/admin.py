from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.storemeta import StoreInfo

# Register your models here.

class AdminProduct(admin.ModelAdmin):
    list_display=['name','price','category','is_featured']
    list_editable=['is_featured','price']

class AdminCategory(admin.ModelAdmin):
    list_display=['name']

admin.site.register(Product,AdminProduct)
admin.site.register(Category,AdminCategory)
admin.site.register(StoreInfo)