import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.factories import AccountFactory
from core.factories import CategoryFactory
from core.factories import ClientFactory
from core.factories import MovementFactory
from core.models import Account
from core.models import CategoryClient


class ClientAccountBalanceTestCase(TestCase):
    def setUp(self):
        client = ClientFactory()
        client.save()
        self.account = AccountFactory(client=client)
        self.account.save()
        self.url = reverse("clients_accounts", kwargs={'pk': self.account.client_id})

        movement = MovementFactory(account=self.account)
        movement.save()

    def test_get_account_balance_successfully(self):
        response = self.client.get(
            path=self.url
        )

        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response_json["accounts"][0]["balance"], 1000.0)

    def test_get_account_balance_fails_client_not_found(self):
        url = reverse("clients_accounts", kwargs={'pk': 999})
        response = self.client.get(
            path=url
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_account_balance_success_client_without_account(self):
        client = ClientFactory(name="Pepe Reina")
        client.save()
        url = reverse("clients_accounts", kwargs={'pk': client.id})
        response = self.client.get(
            path=url
        )

        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response_json["accounts"]), 0)


class ClientListCreateTestCase(TestCase):
    def setUp(self):
        self.url = reverse("clients")
        self.data = {
            "name": "Pedro Arroyo"
        }

    def test_create_client_success(self):
        response = self.client.post(
            path=self.url,
            data=self.data,
            content_type="application/json"
        )

        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_json["name"], self.data["name"])
        self.assertEqual(Account.objects.filter(client_id=response_json["id"]).count(), 1)

    def test_create_client_fails_invalid_data(self):
        response = self.client.post(
            path=self.url,
            data={},
            content_type="application/json"
        )

        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", response_json["name"])

    def test_get_clients_empty_success(self):
        response = self.client.get(
            path=self.url
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response_json) == 0)

    def test_get_clients_with_data_success(self):
        client = ClientFactory()
        client.save()

        response = self.client.get(
            path=self.url
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response_json) > 0)
        self.assertEqual(response_json[0]["name"], client.name)

class ClientDetailUpdateTestCase(TestCase):
    def setUp(self):
        self.new_client = ClientFactory()
        self.new_client.save()
        account = AccountFactory(client=self.new_client)
        account.save()
        category = CategoryFactory()
        category.save()
        CategoryClient.objects.create(client=self.new_client,
                                      category=category)

        self.url = reverse("clients_detail", kwargs={'pk': self.new_client.id})

    def test_get_specific_client_data_success(self):
        response = self.client.get(
            path=self.url
        )

        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["client"]["id"], self.new_client.id)
        self.assertTrue(len(response_json["account"]) > 0)
        self.assertEqual(len(response_json["categories"]), 1)

    def test_get_specific_client_data_fails_client_not_found(self):
        url = reverse("clients_detail", kwargs={'pk': 999})
        response = self.client.get(
            path=url
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_specific_client_without_category_success(self):
        client_without_category = ClientFactory()
        client_without_category.save()

        url = reverse("clients_detail", kwargs={'pk': client_without_category.id})

        response = self.client.get(
            path=url
        )

        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["client"]["id"], client_without_category.id)
        self.assertEqual(len(response_json["categories"]), 0)

    def test_update_client_data_success(self):
        data = {
            "name": "Pedro Arroyo"
        }

        response = self.client.put(
            path=self.url,
            data=data,
            content_type="application/json"
        )

        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["id"], self.new_client.id)
        self.assertEqual(response_json["name"], data["name"])

    def test_update_client_data_fails_name_not_provided(self):
        response = self.client.put(
            path=self.url,
            data={},
            content_type="application/json"
        )

        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", response_json["name"])

    def test_update_client_data_fails_client_not_found(self):
        url = reverse("clients_detail", kwargs={'pk': 999})
        data = {
            "name": "Pedro Arroyo"
        }

        response = self.client.get(
            path=url,
            data=data,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_client_success(self):
        response = self.client.delete(
            path=self.url
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_client_fails_client_not_found(self):
        url = reverse("clients_detail", kwargs={'pk': 999})

        response = self.client.delete(
            path=url
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ClientCategoryAssignmentTestCase(TestCase):
    def setUp(self):
        self.new_client = ClientFactory()
        self.new_client.save()
        self.category = CategoryFactory()
        self.category.save()

        self.data = {
            "client": self.new_client.id,
            "category": self.category.id
        }

        self.url = reverse("clients_category")

    def test_category_assignment_success(self):
        response = self.client.post(
            path=self.url,
            data=self.data,
            content_type="application/json"
        )

        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_json["client"]["id"], self.new_client.id)
        self.assertEqual(response_json["category"]["id"], self.category.id)

    def test_category_assignment_fails_client_not_found(self):
        data = {
            "client": 999,
            "category": self.category.id
        }

        response = self.client.post(
            path=self.url,
            data=data,
            content_type="application/json"
        )

        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid pk \"999\" - object does not exist.", response_json["client"])

    def test_category_assignment_fails_category_not_found(self):
        data = {
            "client": self.new_client.id,
            "category": 998
        }

        response = self.client.post(
            path=self.url,
            data=data,
            content_type="application/json"
        )

        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid pk \"998\" - object does not exist.", response_json["category"])
