from django.db import models


# max_length includes extra space to avoid unexpected error due to new dataset
# max_length for existing dataset
# name 18
class Ingredient(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    oily = models.SmallIntegerField()
    dry = models.SmallIntegerField()
    sensitive = models.SmallIntegerField()


# max_length for existing dataset
# imageId 36
# name 70
# gender 6
# category 10
class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    imageId = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    gender = models.CharField(max_length=10)
    category = models.CharField(max_length=20)
    monthlySales = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredient)
