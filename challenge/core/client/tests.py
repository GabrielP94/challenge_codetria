from django.test import TestCase

from core.models import Account
from core.models import Client
from core.models import Movement


class ClientAccountBalanceTestCase(TestCase):
    def test_response_with_serialized_client_and_account_balances(self):
        # Arrange
        client = Client.objects.create(name="John Doe")
        account = Account.objects.create(client=client, balance=100.0)
        Movement.objects.create(account=account, movement_type="cash_inflow", amount=50.0)
        Movement.objects.create(account=account, movement_type="cash_outflow", amount=25.0)

        # Act
        response = self.client.get(f"/api/client/{client.id}/balance/")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["client"]["id"], client.id)
        self.assertEqual(response.data["client"]["name"], client.name)
        self.assertEqual(len(response.data["accounts"]), 1)
        self.assertEqual(response.data["accounts"][0]["account"], account.id)
        self.assertEqual(response.data["accounts"][0]["balance"], 25.0)

    def test_empty_list_of_account_balances_for_client_with_no_accounts(self):
        # Arrange
        client = Client.objects.create(name="John Doe")

        # Act
        response = self.client.get(f"/api/client/{client.id}/balance/")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["client"]["id"], client.id)
        self.assertEqual(response.data["client"]["name"], client.name)
        self.assertEqual(len(response.data["accounts"]), 0)

    def test_balance_of_zero_for_account_with_no_movements(self):
        # Arrange
        client = Client.objects.create(name="John Doe")
        account = Account.objects.create(client=client, balance=100.0)

        # Act
        response = self.client.get(f"/api/client/{client.id}/balance/")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["client"]["id"], client.id)
        self.assertEqual(response.data["client"]["name"], client.name)
        self.assertEqual(len(response.data["accounts"]), 1)
        self.assertEqual(response.data["accounts"][0]["account"], account.id)
        self.assertEqual(response.data["accounts"][0]["balance"], 0.0)

    def test_balance_of_zero_for_account_with_no_movements(self):
        # Arrange
        client = Client.objects.create(name="John Doe")
        account = Account.objects.create(client=client, balance=100.0)

        # Act
        response = self.client.get(f"/api/client/{client.id}/balance/")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["client"]["id"], client.id)
        self.assertEqual(response.data["client"]["name"], client.name)
        self.assertEqual(len(response.data["accounts"]), 1)
        self.assertEqual(response.data["accounts"][0]["account"], account.id)
        self.assertEqual(response.data["accounts"][0]["balance"], 0.0)

    def test_200_response_with_empty_list_of_accounts_for_nonexistent_client_id(self):
        nonexistent_client_id = 999

        response = self.client.get(f"/api/client/{nonexistent_client_id}/balance/")

        self.assertEqual(response.status_code, 404)
