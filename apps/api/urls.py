from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r"^products/$", views.products, name="products"),
    re_path(r"^product/(?P<id>\w+)/$", views.product, name="product"),
    # extra endpoint for data validation
    re_path(r"^test/data/(?P<id>\w+)/$", views.test_data, name="test_data"),
]
