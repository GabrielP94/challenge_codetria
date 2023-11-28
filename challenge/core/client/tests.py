import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.factories import AccountFactory
from core.factories import ClientFactory
from core.factories import MovementFactory
from core.models import Account


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
