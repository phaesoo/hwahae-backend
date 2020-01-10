from rest_framework import serializers
from .models import Item, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "oily", "dry", "sensitive"]


class ItemSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=True, read_only=True)
    class Meta:
        model = Item
        fields = ["id", "imageId", "name", "price", "gender", "category", "monthlySales", "ingredient"]
