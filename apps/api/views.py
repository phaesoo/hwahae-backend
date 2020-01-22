from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from django.db.models import Sum
from rest_framework.exceptions import NotFound
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.common.exceptions import InvalidQueryParam, DatabaseError
from .models import Item
from .serializers import ItemSerializer, TestItemSerializer
from . import configs


# query parameters
param_skin_type = openapi.Parameter('skin_type', openapi.IN_QUERY, description="['oily', 'sensitive', 'dry']", type=openapi.TYPE_STRING, required=True)
param_category = openapi.Parameter('category', openapi.IN_QUERY, description="Cosmetic category", type=openapi.TYPE_STRING)
param_page = openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER)
param_exclude_ingredient = openapi.Parameter('exclude_ingredient', openapi.IN_QUERY, description="Ingredient list which have to be excluded(comma separated)", type=openapi.TYPE_STRING)
param_include_ingredient = openapi.Parameter('include_ingredient', openapi.IN_QUERY, description="Ingredient list which have to be included(comma separated)", type=openapi.TYPE_STRING)


@swagger_auto_schema(
    methods=["get"], 
    operation_description="API for getting cosmetic informations satisfying given conditions. (order by high-score desc.)",
    manual_parameters=[
        param_skin_type,
        param_category,
        param_page,
        param_exclude_ingredient,
        param_include_ingredient,
    ])
@api_view(["GET"])
def products(request):
    # query params
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
        paginator.page_size = settings.QUERY_PAGE_SIZE
        querysets = paginator.paginate_queryset(querysets, request)

    # serializing
    serializer = ItemSerializer(
        querysets, 
        many=True, 
        fields=["id", "imgUrl", "name", "price", "ingredients", "monthlySales"], 
        image_type="thumbnail"
        )

    if not len(serializer.data):
        raise NotFound
    
    return Response(serializer.data)


@swagger_auto_schema(
    methods=["get"], 
    operation_description="API for getting detail information of target item(=id) and 3 recommended item summary.",
    manual_parameters=[
        param_skin_type,
    ])
@api_view(["GET"])
def product(request, id):
    # query params
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
    rec_items = Item.objects.filter(category=category).annotate(
        score=Sum("ingredients__{}".format(skin_type))).order_by("-score", "price")[:3]

    # serializing
    main_serializer = ItemSerializer(main_item, many=True, image_type="image")
    sub_serializer = ItemSerializer(rec_items, many=True, image_type="thumbnail", fields=["id", "imgUrl", "name", "price"])
    
    # return merged result
    return Response(main_serializer.data + sub_serializer.data)


# extra endpoint for data validation
@swagger_auto_schema(
    methods=["get"], 
    operation_description="Test API for a data validation",
    manual_parameters=[
        param_skin_type,
    ])
@api_view(["GET"])
def test_data(request, id):
    # query params
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

    # queryset for recommended item
    rec_items = Item.objects.filter(category=category).annotate(
        score=Sum("ingredients__{}".format(skin_type))).order_by("-score", "price")[:3]

    # serializing
    main_serializer = TestItemSerializer(main_item, many=True, fields=["id", "name", "price", "category", "ingredients"])
    sub_serializer = TestItemSerializer(rec_items, many=True)

    return Response(main_serializer.data + sub_serializer.data)