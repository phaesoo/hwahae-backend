from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum
from apps.common.exceptions import InvalidQueryParam, DatabaseError
from .models import Item
from .serializers import ItemSerializer
from . import configs


@api_view(["GET"])
def products(request):
    skin_type = request.query_params.get("skin_type")
    if skin_type is None:
        raise InvalidQueryParam("skin_type should be specified")
    elif skin_type not in configs.SKIN_TYPES:
        raise InvalidQueryParam("Invalid query param: skin_type")
    category = request.query_params.get("category")
    page = request.query_params.get("page")
    exclude_ingredient = request.query_params.get("exclude_ingredient")
    include_ingredient = request.query_params.get("include_ingredient")

    # querysets
    querysets = Item.objects.all()
    if category is not None:
        querysets = querysets.filter(category=category)

    def preprocessing(param):
        param_list = param.split(",")
        # remove left/right space
        return [param.strip() for param in param_list]

    if exclude_ingredient is not None:
        querysets = querysets.exclude(ingredients__name__in=preprocessing(exclude_ingredient))

    if include_ingredient is not None:
        querysets = querysets.filter(ingredients__name__in=preprocessing(include_ingredient))

    # sum by skin_type and ordering(score desc, price asc)
    querysets = querysets.annotate(score=Sum("ingredients__{}".format(skin_type))).order_by("-score", "price")

    # paging
    if page is not None:
        try:
            page = int(page)
        except:
            raise InvalidQueryParam("Invalid query param: page")

        paginator = PageNumberPagination()
        paginator.page_size = 50
        querysets = paginator.paginate_queryset(querysets, request)

    # serializing
    serializer = ItemSerializer(
        querysets, 
        many=True, 
        fields=["id", "imgUrl", "name", "price", "ingredients", "monthlySales"], 
        image_type="thumbnail"
        )
    return Response(serializer.data)

@api_view(["GET"])
def product(request, id):
    try:
        id = int(id)
    except:
        raise InvalidQueryParam("Invalid query param: id={}".format(id))

    skin_type = request.query_params.get("skin_type")
    if skin_type is None:
        raise InvalidQueryParam("skin_type should be specified")
    elif skin_type not in configs.SKIN_TYPES:
        raise InvalidQueryParam("Invalid query param: skin_type={}".format(skin_type))

    # queryset for main item
    main_item = Item.objects.filter(id=id)
    item_num = len(main_item)
    if item_num == 1:
        category = main_item[0].category
    elif item_num == 0:
        raise InvalidQueryParam("id not found: id={}".format(id))
    else:
        raise DatabaseError("Duplicated row in DB: id={}".format(id))

    # queryset for sub item
    sub_items = Item.objects.filter(category=category).annotate(
        score=Sum("ingredients__{}".format(skin_type))).order_by("-score", "price")[:3]

    # serializing
    main_serializer = ItemSerializer(main_item, many=True, image_type="image")
    sub_serializer = ItemSerializer(sub_items, many=True, image_type="thumbnail", fields=["id", "imgUrl", "name", "price"])
    
    # return merged result
    return Response(main_serializer.data + sub_serializer.data)
