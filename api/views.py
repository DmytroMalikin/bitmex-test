import json
import bitmex
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from bitmex_api.models import Account
from api.serializers import OrderSerializer


def check_account(func):
    def wrapper(instance, request, *args, **kwargs):
        name = request.query_params.get('account')
        account = get_object_or_404(Account.objects.all(), name=name)
        instance.client = bitmex.bitmex(test=True, api_key=account.api_key, api_secret=account.api_secret)
        return func(instance, request, *args, **kwargs)

    return wrapper


class OrderViewSet(viewsets.ViewSet):
    client = None

    @check_account
    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = self.client.Order.Order_new(**serializer.validated_data).result()[0]

        response_serializer = OrderSerializer(data)
        return Response(response_serializer.data)

    @check_account
    def list(self, request):
        data = self.client.Order.Order_getOrders(count=5, reverse=True).result()[0]
        serializer = OrderSerializer(data, many=True)
        return Response(serializer.data)

    @check_account
    def retrieve(self, request, pk=None):
        data = self.client.Order.Order_getOrders(filter=json.dumps({"orderID": pk})).result()[0][0]
        serializer = OrderSerializer(data)
        return Response(serializer.data)

    @check_account
    def destroy(self, request, pk=None):
        data = self.client.Order.Order_cancel(orderID=pk).result()
        print(data)
        serializer = OrderSerializer(data)
        return Response(serializer.data)
