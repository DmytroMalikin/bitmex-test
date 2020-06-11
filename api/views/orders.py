import bitmex
from bravado.exception import HTTPBadRequest
from rest_framework import viewsets, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.serializers import BitmexOrderSerializer, OrderSerializer
from bitmex_api.models import Account, Order


def check_account(func):
    def wrapper(instance, request, *args, **kwargs):
        name = request.query_params.get('account')
        account = get_object_or_404(Account.objects.all(), name=name)
        instance.client = bitmex.bitmex(test=True, api_key=account.api_key, api_secret=account.api_secret)
        instance.account = account
        return func(instance, request, *args, **kwargs)

    return wrapper


class OrderViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    client = None
    account = None

    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(account__name=self.account.name).order_by('timestamp')[:5]

    @check_account
    def create(self, request):
        serializer = BitmexOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            data = self.client.Order.Order_new(**serializer.validated_data).result()[0]
        except HTTPBadRequest as e:
            raise ValidationError({
                'detail': e.swagger_result.get('error', {}).get('message', "Couldn't create Order")
            })

        order = Order.objects.create(
            order_id=data.get('orderID'),
            symbol=data.get('symbol'),
            volume=data.get('orderQty'),
            side=data.get('side') == 'Sell',
            price=data.get('price'),
            account=self.account,
        )

        response_serializer = self.get_serializer(order)
        return Response(response_serializer.data)

    @check_account
    def list(self, request, *args, **kwargs):
        return super(OrderViewSet, self).list(request, *args, **kwargs)

    @check_account
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super(OrderViewSet, self).list(request, pk=pk, *args, **kwargs)

    @check_account
    def destroy(self, request, pk=None, *args, **kwargs):
        data = self.client.Order.Order_cancel(orderID=pk).result()
        print(data)

        return super(OrderViewSet, self).destroy(request, pk=pk, *args, **kwargs)
