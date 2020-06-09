from rest_framework import serializers
from bitmex_api.models import Account, Order


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'name',
        )


class OrderSerializer(serializers.Serializer):
    orderID = serializers.CharField(required=False)
    symbol = serializers.CharField(required=True)
    ordType = serializers.CharField(required=True)
    orderQty = serializers.IntegerField(required=True)
    side = serializers.CharField(required=True)

    def validate_side(self, value):
        if value not in Order.side_validation_types:
            raise serializers.ValidationError(f'should be one of these types {str(Order.side_validation_types)}')
