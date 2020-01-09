from rest_framework import viewsets
from .serializers import *
from .models import *


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()[:5]
    serializer_class = IngredientSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()[:5]
    serializer_class = ItemSerializer
