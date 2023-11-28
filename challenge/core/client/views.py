from django.http import Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from core.client.serializers import ClientSerializer
from core.client.serializers import FullClientInformationSerializer
from core.client.serializers import CategoryClientRequestSerializer
from core.client.utils import get_account_balance
from core.models import Account
from core.models import CategoryClient
from core.models import Client


class ClientListCreate(APIView):
    """
    This view lists all clients and allows you to create a new one.

    To Create, the JSON structure is:

        {"name": "Nombre Ficticio"}

    """
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            client_id = Client.objects.last().id
            client_account = Account.objects.create(client_id=client_id)
            client_account.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientDetailUpdate(APIView):
    """
    This view returns specific client information and allows you to delete it and update it.

     * NOTE: You can update only the client name

    """
    def get(self, request, pk):
        client = get_object_or_404(Client.objects.all(), pk=pk)
        account = Account.objects.filter(client_id=client.id)
        category = CategoryClient.objects.filter(client_id=client.id)
        data = {
            "client": client,
            "account": account,
            "categories": category
        }
        serializer = FullClientInformationSerializer(data)
        return Response(serializer.data)

    def put(self, request, pk):
        client = get_object_or_404(Client.objects.all(), pk=pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = get_object_or_404(Client.objects.all(), pk=pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientCategoryAssignment(APIView):
    """
    This view allows you to assign a category to a specific client.

    The JSON Structure is:

        {"client": 1, "category": 1}

    """
    def post(self, request):
        serializer = CategoryClientRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientAccountBalance(APIView):
    def get(self, request, pk):
        client = get_object_or_404(Client.objects.all(), pk=pk)

        accounts = Account.objects.filter(client_id=client.id)

        account_list = []

        for account in accounts:
            account_balance = {
                "account": account.id,
                "balance": get_account_balance(account.id)
            }
            account_list.append(account_balance)

        return Response({"client": ClientSerializer(client).data,
                         "accounts": account_list})
