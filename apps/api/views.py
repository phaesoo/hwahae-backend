from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from apps.common.response import success, error
from .models import Item, Ingredient
from .serializers import ItemSerializer, IngredientSerializer

@api_view(["GET"])
def products(request):
    skin_type = request.query_params.get("skin_type")
    category = request.query_params.get("category")
    page = request.query_params.get("page")
    exclude_ingredient = request.query_params.get("exclude_ingredient")
    include_ingredient = request.query_params.get("include_ingredient")

    print (skin_type, category, page, type(page))

    # prepare for querysets
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

    if page is not None:
        try:
            page = int(page)
        except:
            raise TypeError

        paginator = PageNumberPagination()
        paginator.page_size = 50
        result_page = paginator.paginate_queryset(querysets, request)
        serializer = ItemSerializer(result_page, many=True)
        print (result_page, serializer)

    return Response({"temp": 1})