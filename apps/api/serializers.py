from rest_framework import serializers
from urllib.parse import urljoin
from .models import Item
from .configs import BASE_IMG_URL
from apps.common.serializers import DynamicFieldsModelSerializer


class ItemSerializer(DynamicFieldsModelSerializer):
    __valid_image_types = ["image", "thumbnail"]
    imgUrl = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        # Don't pass the 'image_type' arg up to the superclass
        image_type = kwargs.pop("image_type", "image")
        # validate image type
        if image_type not in ItemSerializer.__valid_image_types:
            raise ValueError(image_type)
        self.__image_type = image_type

        super(ItemSerializer, self).__init__(*args, **kwargs)

    def get_imgUrl(self, instance):
        return urljoin(BASE_IMG_URL, "2020-birdview/{}/{}.jpg".format(self.__image_type, instance.imageId))

    def get_ingredients(self, instance):
        queryset = instance.ingredients.get_queryset()
        return ",".join([a.name for a in queryset])

    class Meta:
        model = Item
        fields = ["id", "imgUrl", "name", "price", "gender", "category", "ingredients", "monthlySales"]
