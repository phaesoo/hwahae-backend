from rest_framework import serializers
from urllib.parse import urljoin
from .models import Item, Ingredient
from .configs import BASE_IMG_URL


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


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
        return urljoin(BASE_IMG_URL, "{}/{}.jpg".format(self.__image_type, instance.imageId))

    def get_ingredients(self, instance):
        queryset = instance.ingredients.get_queryset()
        return ",".join([a.name for a in queryset])

    class Meta:
        model = Item
        fields = ["id", "imgUrl", "name", "price", "gender", "category", "monthlySales", "ingredients"]


"""
class ItemSerializer(serializers.ModelSerializer):
    imgUrl = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()

    def get_imgUrl(self, instance):
        return "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/{}.jpg".format(instance.imageId)

    def get_ingredients(self, instance):
        queryset = instance.ingredients.get_queryset()
        return ",".join([a.name for a in queryset])
    
    class Meta:
        model = Item
        fields = ["id", "imgUrl", "name", "price", "gender", "category", "monthlySales", "ingredients"]
"""