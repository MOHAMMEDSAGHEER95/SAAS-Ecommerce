from rest_framework import serializers

from basket.models import Basket, BasketLine
from orders.models import ShippingAddress, Order
from products.models import Products


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('title', 'description', 'price', 'get_image_url')


class ProductsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'title', 'description', 'price', 'get_image_url')



class BasketLineSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    class Meta:
        model = BasketLine
        fields = ('basket', 'product', 'quantity', 'price')


class BasketAddProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasketLine
        fields = ('product', 'quantity', 'basket')



class BasketSerializers(serializers.ModelSerializer):
    lines = BasketLineSerializer(many=True, read_only=True)
    class Meta:
        model = Basket
        fields = ('id', 'status', 'user', 'lines', 'total')


class ShippingAddressSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = ShippingAddress
        fields = ('id', 'line_1', 'line_2', 'city', 'postcode', 'user', 'is_default')


class OrderSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    number = serializers.ReadOnlyField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    basket = BasketSerializers()

    class Meta:
        model = Order
        fields = ('id', 'basket', 'number', 'user', 'shipping_address', 'total_incl_tax')


class StripetokenSerializers(serializers.Serializer):
    stripe_token = serializers.CharField(required=True)


class CreateOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('shipping_address', 'basket')