from rest_framework import serializers

from core.models import Client, Account, Category, CategoryClient


class ClientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=500, required=True)

    class Meta:
        model = Client
        fields = ['id', 'name']


class AccountSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta:
        model = Account
        fields = ["id", "client"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CategoryClientSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = CategoryClient
        fields = ["category"]


class CategoryClientRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryClient
        fields = ["client", "category"]

    def to_representation(self, instance):
        rep = super(CategoryClientRequestSerializer, self).to_representation(instance)

        rep["client"] = ClientSerializer(Client.objects.get(pk=rep["client"])).data
        rep["category"] = CategorySerializer(Category.objects.get(pk=rep["category"])).data

        return rep


class FullClientInformationSerializer(serializers.Serializer):
    client = ClientSerializer()
    account = AccountSerializer(many=True)
    categories = CategoryClientSerializer(many=True)
