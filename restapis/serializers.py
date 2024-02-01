from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']
        if product.stock < quantity:
            raise serializers.ValidationError("Not enough stock available.")
        return data



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
    created_at = serializers.ReadOnlyField()
    tracking_url = serializers.ReadOnlyField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    basket = BasketSerializers()

    class Meta:
        model = Order
        fields = ('id', 'basket', 'number', 'user', 'shipping_address', 'total_incl_tax', 'tracking_url', 'created_at')


class StripetokenSerializers(serializers.Serializer):
    stripe_token = serializers.CharField(required=True)


class CreateOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('shipping_address', 'basket')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] =self.user.id
        return data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': False},
        }

    def validate(self, data):
        """
        Validate that the passwords match and set the username as the email.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")

        # Set username as the email address
        data['username'] = data['email']

        return data
    def create(self, validated_data):
        """
        Create a new user with the validated data, and remove 'password2'.
        """
        validated_data.pop('password2', None)
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
