from rest_framework import serializers

from basket.models import Basket, BasketLine
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