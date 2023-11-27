from rest_framework import serializers

from core.client.serializers import AccountSerializer
from core.models import Account
from core.models import Movement


class MovementSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Movement
        fields = ["id", "account", "movement_type", "amount"]

    def validate(self, data):
        # ToDo: Use this function to validate amount and balance

        return data

    def to_representation(self, instance):
        rep = super(MovementSerializer, self).to_representation(instance)

        rep["movement_type"] = instance.get_movement_type_display()
        rep["account"] = AccountSerializer(Account.objects.get(pk=rep["account"])).data

        return rep
