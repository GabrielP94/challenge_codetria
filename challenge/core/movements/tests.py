import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.client.utils import get_account_balance
from core.factories import AccountFactory
from core.factories import ClientFactory
from core.factories import MovementFactory


class MovementCreateTestCase(TestCase):
    def setUp(self):
        client = ClientFactory()
        client.save()
        self.account = AccountFactory(client=client)
        self.account.save()

        self.url = reverse("movements")
        self.data = {
            "account": self.account.id,
            "movement_type": "cash_inflow",
            "amount": 10000
        }

    def test_create_movement_success(self):
        response = self.client.post(
            path=self.url,
            data=self.data,
            content_type="application/json"
        )

        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_json["amount"], 10000)
        self.assertEqual(response_json["account"]["id"], self.account.id)
        self.assertEqual(get_account_balance(self.account.id), 10000)

    def test_create_movement_fails_invalid_amount(self):
        movement = MovementFactory(
            account=self.account,
            movement_type="cash_inflow",
            amount=2000
        )
        movement.save()

        data = {
            "account": self.account.id,
            "movement_type": "cash_outflow",
            "amount": 10000
        }
        response = self.client.post(
            path=self.url,
            data=data,
            content_type="application/json"
        )

        response_json = json.loads(response.content)
        self.assertEqual(get_account_balance(self.account.id), 2000)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Your account balance is lower than the amount that you want to extract.",
                      response_json["field_amount"])

    def test_create_movement_fails_invalid_account(self):
        data = {
            "account": 999,
            "movement_type": "cash_inflow",
            "amount": 10000
        }
        response = self.client.post(
            path=self.url,
            data=data,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MovementDetailDeleteTestCase(TestCase):
    def setUp(self):
        client = ClientFactory()
        client.save()
        self.account = AccountFactory(client=client)
        self.account.save()

    def test_get_movement_data_success(self):
        movement = MovementFactory(account=self.account)
        movement.save()

        url = reverse("movements_detail", kwargs={'pk': movement.id})

        response = self.client.get(
            path=url
        )

        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["amount"], movement.amount)
        self.assertEqual(response_json["movement_type"], movement.get_movement_type_display())

    def test_get_movement_data_fails_movement_not_found(self):

        url = reverse("movements_detail", kwargs={'pk': 999})

        response = self.client.get(
            path=url
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_movement_data_success(self):
        movement = MovementFactory(account=self.account,
                                   amount=2000)
        movement.save()

        url = reverse("movements_detail", kwargs={'pk': movement.id})

        response = self.client.delete(
            path=url
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_account_balance(self.account.id), 0.0)

    def test_delete_movement_data_fails_movement_not_found(self):

        url = reverse("movements_detail", kwargs={'pk': 999})

        response = self.client.delete(
            path=url
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
