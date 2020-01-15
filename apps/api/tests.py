from django.urls import reverse
from rest_framework.test import APITestCase


class ProductTests(APITestCase):
    fixtures = ['item.json', "ingredient.json"]

    def test_product(self):
        url = "{}?skin_type=oily".format(reverse("product", args=[3]))
        response = self.client.get(url)

    def test_products(self):
        url = "{}?skin_type=oily".format(reverse("products"))
        response = self.client.get(url)
