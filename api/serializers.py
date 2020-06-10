from rest_framework import serializers

from bitmex_api.models import Account, Order


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'name',
        )


class BitmexOrderSerializer(serializers.Serializer):
    orderID = serializers.CharField(required=False)
    symbol = serializers.CharField(required=True)
    ordType = serializers.CharField(required=True)
    orderQty = serializers.IntegerField(required=True)
    side = serializers.CharField(required=True)
    price = serializers.CharField(required=False)

    def validate_side(self, value):
        if value not in Order.side_validation_types:
            raise serializers.ValidationError(f'should be one of these types {str(Order.side_validation_types)}')


class OrderSerializer(serializers.ModelSerializer):
    side = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'order_id', 'symbol',
            'volume', 'side', 'price',
            'timestamp', 'account'
        )

    def get_side(self, obj):
        return 'Sell' if obj.side else 'Buy'
