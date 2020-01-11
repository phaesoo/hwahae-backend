from rest_framework import serializers
from .models import Item, Ingredient


class ItemSerializer(serializers.ModelSerializer):
    ingredient_list = serializers.SerializerMethodField()
    def get_ingredient_list(self, instance):
            queryset = instance.ingredients.get_queryset()
            return ",".join([a.name for a in queryset])
    class Meta:
        model = Item
        fields = ["id", "imageId", "name", "price", "gender", "category", "monthlySales", "ingredient_list"]
