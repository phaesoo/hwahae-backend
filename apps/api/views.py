from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum
from apps.common.response import success, error
from .models import Item
from .serializers import ItemSerializer
from . import configs


@api_view(["GET"])
def products(request):
    skin_type = request.query_params.get("skin_type")
    if skin_type not in configs.SKIN_TYPES:
        raise ValueError
    category = request.query_params.get("category")
    page = request.query_params.get("page")
    exclude_ingredient = request.query_params.get("exclude_ingredient")
    include_ingredient = request.query_params.get("include_ingredient")

    # querysets
    querysets = Item.objects.all()
    if category is not None:
        querysets = querysets.filter(category=category)

    def preprocessing(param):
        if not isinstance(param, str):
            raise ValueError
        param_list = param.split(",")
        # remove left/right space
        return [param.strip() for param in param_list]

    if exclude_ingredient is not None:
        querysets.exclude(ingredient__name__in=preprocessing(exclude_ingredient))

    if include_ingredient is not None:
        querysets.filter(ingredient__name__in=preprocessing(include_ingredient))

    # sum by skin_type and ordering(score desc, price asc)
    querysets = querysets.annotate(score=Sum("ingredients__{}".format(skin_type))).order_by("-score", "price")

    # paging
    if page is not None:
        try:
            page = int(page)
        except:
            raise TypeError

        paginator = PageNumberPagination()
        paginator.page_size = 50
        querysets = paginator.paginate_queryset(querysets, request)

    #for i in querysets:
    #    print (i.name, i.score)

    serializer = ItemSerializer(
        querysets, 
        many=True, 
        fields=["id", "imgUrl", "name", "price", "ingredients", "monthlySales"], 
        image_type="thumbnail"
        )
    return success(serializer.data)

@api_view(["GET"])
def product(request, id):
    try:
        id = int(id)
    except:
        raise ValueError

    skin_type = request.query_params.get("skin_type")
    if skin_type not in configs.SKIN_TYPES:
        raise ValueError

    # querysets
    main_item = Item.objects.filter(id=id)
    item_num = len(main_item)
    if item_num == 1:
        category = main_item[0].category
    elif item_num == 0:
        raise ValueError
    else:
        raise ValueError

    sub_items = Item.objects.filter(category=category).annotate(
        score=Sum("ingredients__{}".format(skin_type))).order_by("-score", "price")[:3]

    main_serializer = ItemSerializer(main_item, many=True, image_type="image")
    sub_serializer = ItemSerializer(sub_items, many=True, image_type="thumbnail", fields=["id", "imgUrl", "name", "price"])
    
    return success(main_serializer.data + sub_serializer.data)
