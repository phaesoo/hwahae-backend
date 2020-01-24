import os
import pandas as pd
import json
import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.conf import settings


class ProductTests(APITestCase):
    # fixtures for testing db
    fixtures = ['item.json', "ingredient.json"]

    def test_product(self):
        # input
        invalid_skin_type = "test"
        skin_type = "oily"
        args = [3]

        main_response_format = {
            "id": int,
            "imgUrl": str,
            "name": str,
            "price": int,
            "gender": str,
            "category": str,
            "ingredients": str,
            "monthlySales": int,
        }

        rec_response_format = {
            "id": int,
            "imgUrl": str,
            "name": str,
            "price": int,
        }

        ######################################################################
        # api call test (fail), without specifying skin_type
        url = "{}".format(reverse("product", args=args))
        response = self.client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        ######################################################################
        # api call test (fail), invalid skin_type
        url = "{}?skin_type={}".format(reverse("product", args=args), invalid_skin_type)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        ######################################################################
        # api call test (success)
        url = "{}?skin_type={}".format(reverse("product", args=args), skin_type)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # response content validation
        result = json.loads(response.content.decode("utf-8"))
        assert isinstance(result, list)
        assert len(result) == 4

        main_item = result[0]
        rec_items = result[1:]

        # validate main item (key, format)
        assert set(main_response_format.keys()) == set(main_item.keys())
        for key in main_response_format:
            assert isinstance(main_item[key], main_response_format[key])

        # image url validation and request test
        img_url = main_item["imgUrl"]
        assert "image" in img_url
        assert requests.get(img_url).status_code == status.HTTP_200_OK

        # validate recommended items
        key_list = set(rec_response_format.keys())
        for item in rec_items:
            assert key_list == set(item.keys())
            for key in rec_response_format:
                assert isinstance(item[key], rec_response_format[key])

            # image url validation and request test
            img_url = item["imgUrl"]
            assert "thumbnail" in img_url
            assert requests.get(img_url).status_code == status.HTTP_200_OK

    def test_products(self):
        # input
        invalid_skin_type = "test"
        invalid_page = 0
        invalid_category = "category"
        skin_type = "sensitive"
        page = 1
        category = "maskpack"
        include_ingredient = ["challenge", "unique"]
        exclude_ingredient = ["attractive", "frequency"]

        response_format = {
            "id": int,
            "imgUrl": str,
            "name": str,
            "price": int,
            "ingredients": str,
            "monthlySales": int,
        }

        ######################################################################
        # api call test (fail), without specifying skin_type
        url = "{}".format(reverse("products"))
        response = self.client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        ######################################################################
        # api call test (fail), invalid skin_type
        url = "{}?skin_type={}".format(reverse("products"), invalid_skin_type)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        ######################################################################
        # api call test (success) with skin_type
        url = "{}?skin_type={}".format(reverse("products"), skin_type)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # data validation (key and type)
        results = json.loads(response.content.decode("utf-8"))
        assert isinstance(results, list)
        assert len(results)

        # check first 10 items
        key_list = set(response_format.keys())
        for result in results[:10]:
            # key check
            assert key_list == set(result.keys())
            # format check
            for key in response_format:
                assert isinstance(result[key], response_format[key])

        ######################################################################
        # api call test (fail) with skin_type, invalid_page
        url = "{}?skin_type={}&page={}".format(reverse("products"), skin_type, invalid_page)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        ######################################################################
        # api call test (success) with skin_type, page
        url = "{}?skin_type={}&page={}".format(reverse("products"), skin_type, page)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # data validation
        data = json.loads(response.content.decode("utf-8"))
        assert isinstance(data, list)
        assert len(data) == settings.QUERY_PAGE_SIZE

        ######################################################################
        # api call test (fail) with skin_type, category
        url = "{}?skin_type={}&category={}".format(reverse("products"), skin_type, invalid_category)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        ######################################################################
        # api call test (success) with skin_type, category
        url = "{}?skin_type={}&category={}".format(reverse("products"), skin_type, category)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        ######################################################################
        # api call test (success) with skin_type, include_ingredient
        url = "{}?skin_type={}&include_ingredient={}".format(reverse("products"), skin_type, ",".join(include_ingredient))
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # response content validation, should include target ingredients
        results = json.loads(response.content.decode("utf-8"))
        assert isinstance(results, list)
        assert len(results)

        for result in results:
            ingredients = result["ingredients"]
            for ingr in include_ingredient:
                assert ingr in ingredients

        ######################################################################
        # api call test (success) with skin_type, exclude_ingredient
        url = "{}?skin_type={}&exclude_ingredient={}".format(reverse("products"), skin_type, ",".join(exclude_ingredient))
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK       

        # response content validation, should exclude target ingredients
        results = json.loads(response.content.decode("utf-8"))
        assert isinstance(results, list)
        assert len(results)

        for result in results:
            ingredients = result["ingredients"]
            for ingr in exclude_ingredient:
                assert ingr not in ingredients

        ######################################################################
        # api call test (success) with skin_type, include_ingredient, exclude_ingredient
        include_ingredient = ["sentiment"]

        url = "{}?skin_type={}&include_ingredient={}&exclude_ingredient={}".format(reverse("products"), skin_type, ",".join(include_ingredient), ",".join(exclude_ingredient))
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK       

        # response content validation, should exclude target ingredients
        results = json.loads(response.content.decode("utf-8"))
        assert isinstance(results, list)
        assert len(results)

        for result in results:
            ingredients = result["ingredients"]
            for ingr in include_ingredient:
                assert ingr in ingredients
            for ingr in exclude_ingredient:
                assert ingr not in ingredients

    # unit test for data validation
    # validate for id, category, price for all cases. (total 3000 cases currently)
    # read valid data from predumped cache (notebook/test/valid.pickle)
    def test_data(self):
        print ("[INFO] start data validation for 3000 cases (1000 items * 3 skin types)")

        # read predumped validation object from cache
        filename = os.path.join(os.path.dirname(settings.PROJECT_DIR), "notebook", "test", "valid.pickle")
        valid_df = pd.read_pickle(filename, compression="gzip")

        invalid_id_list = list()

        loop = 0

        skin_types = ["oily", "sensitive", "dry"]
        total_count = len(skin_types) * len(valid_df)

        for index, _ in enumerate(valid_df.index):
            valid_srs = valid_df.iloc[index]
            _id = valid_srs["id"]
            _category = valid_srs["category"]
            _price = valid_srs["price"]

            if loop % 100 == 0:
                print ("[INFO] progress: {}/{} ({:.2f}%)".format(loop, total_count, loop/float(total_count) * 100.0))

            for skin_type in skin_types:
                response = self.client.get(
                    "{}?skin_type={}".format(reverse("test_data", args=[_id]), skin_type)
                )
                try:
                    target_data = json.loads(response.content.decode("utf-8"))
                    assert isinstance(target_data, list)
                    main_item = target_data[0]
                    assert isinstance(main_item, dict)
                    sub_items = target_data[1:]
                    assert len(sub_items) == 3

                    # validate main item
                    assert _id == main_item["id"], "{}, {}".format(_id, main_item["id"])
                    assert _category == main_item["category"], "{}, {}".format(_category, main_item["category"])
                    assert _price == main_item["price"], "{}, {}".format(_price, main_item["price"])

                    # validate sub items (recommended items)
                    sub_df = valid_df[valid_df["category"] == _category].sort_values(by=[skin_type, "price"], ascending=[False, True]).head(3)
                    assert len(sub_df) == 3, "recommended item count == {}(!= 3)".format(len(sub_df))

                    for sub_index, sub_dict in enumerate(sub_items):
                        assert isinstance(sub_dict, dict)
                        sub_srs = sub_df.iloc[sub_index]
                        assert sub_srs["id"] == sub_dict["id"], "{}, {}".format(sub_srs["id"], sub_dict["id"])
                        assert sub_srs[skin_type] == sub_dict["score"], "{}, {}".format(sub_srs[skin_type], sub_dict["score"])
                except Exception as e:
                    print (e)
                    invalid_id_list.append(_id)
                finally:
                    loop += 1

        self.assertEqual(len(invalid_id_list), 0)
        print ("[INFO] End data validation")
