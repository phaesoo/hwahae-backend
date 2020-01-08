from rest_framework import serializers
from api.models import Item, Ingredient, ItemIngredient


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        