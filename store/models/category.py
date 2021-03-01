from django.db import models

class Category(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=50,default='None')

    @staticmethod
    def get_all_category():
        return Category.objects.all()