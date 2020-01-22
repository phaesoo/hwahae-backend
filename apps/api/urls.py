from django.urls import path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from . import views


scheme_view = get_schema_view(
    openapi.Info(
        title="HwaHae API",
        default_version="v1.0",
        description="API Document for the service.",
        contact=openapi.Contact(email="phaesoo@gmail.com"),
    ),
    validators=["flex"],
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    # swagger/ as a default page
    path("", RedirectView.as_view(url="swagger/")),
    # documentations
    path("swagger/", scheme_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", scheme_view.with_ui("redoc", cache_timeout=0)),
    # endpoints
    path("products/", views.products, name="products"),
    path("product/<int:id>", views.product, name="product"),
    path("test/data/<int:id>", views.test_data, name="test_data"), # for data validation
]
