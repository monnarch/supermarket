
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    total = models.BigIntegerField()

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.BigIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

class Items(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shopcard_id = models.BigIntegerField()
    sell_date = models.DateField()

class Shopcard(models.Model):
    date = models.BigIntegerField()
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE)
    total_price = models.BigIntegerField()
    payment = models.CharField(max_length=255)

class Customer(models.Model):
    name = models.CharField(max_length=255)
    location = models.BigIntegerField()
    email = models.BigIntegerField()
    number = models.BigIntegerField()
    date = models.BigIntegerField()
