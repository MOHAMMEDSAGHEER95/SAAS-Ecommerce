import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.core.signing import Signer
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from basket.models import Basket
from orders.models import Order
from products.documents import ProductDocument
from products.models import Products
from restapis.permissions import IsPremiumTenant
from restapis.serializers import BasketSerializers, BasketLineSerializer, ProductsSerializer, ProductsListSerializer, \
    BasketAddProductSerializer, ShippingAddressSerializers, OrderSerializers, StripetokenSerializers, \
    CreateOrderSerializers, CustomTokenObtainPairSerializer, RegisterSerializer


# Create your views here.



class BasketDetailAPIView(RetrieveAPIView):
    queryset = Basket
    serializer_class = BasketSerializers
    permission_classes = [AllowAny, IsPremiumTenant]


    def retrieve(self, request, *args, **kwargs):
        print(request.user)
        instance = self.get_basket(request)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_basket(self, request):
        "Get basket from the request."
        if request.user.is_authenticated:
            basket = self.get_user_basket(request.user)
        else:
            basket = self.get_anonymous_basket(request)
        return basket


    def get_anonymous_basket(self, request):
        try:
            basket_id = request.session.get('anonymous_basket_id')
            if not basket_id:
                basket = Basket.create_basket(request.user)
                request.session['anonymous_basket_id'] = basket.id
                basket_id = basket.id
                return basket
            basket = Basket.objects.get(id=basket_id)
            if basket.status != Basket.OPEN:
                del request.session['anonymous_basket_id']
                basket = Basket.create_basket(request.user)
                request.session['anonymous_basket_id'] = basket.id
                return basket
            return basket
        except Exception as e:
            basket = Basket.create_basket(request.user)
            request.session['anonymous_basket_id'] = basket.id
            return basket



    def get_user_basket(self, user):
        return Basket.get_basket(user)




class LoginTokenAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny, IsPremiumTenant]


    def post(self, request, *args, **kwargs):
        basket_id = request.session.get('anonymous_basket_id')
        response = super().post(request, *args, **kwargs)
        try:
            user = get_object_or_404(User, id=response.data['user'])
            user_basket = Basket.get_basket(user)
            Basket.merge_basket(basket_id, user_basket.id)
        except Exception as e:
            print(e)
        return response


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, IsPremiumTenant)
    serializer_class = RegisterSerializer

class ProductListView(ListAPIView):
    queryset = Products.objects.filter(is_available=True)
    serializer_class = ProductsListSerializer
    permission_classes = [AllowAny, IsPremiumTenant]

class AddProductAPI(CreateAPIView):
    serializer_class = BasketAddProductSerializer
    permission_classes = [AllowAny, IsPremiumTenant]

    def perform_create(self, serializer):
        basket = serializer.validated_data['basket']
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        if not quantity:
            quantity = serializer.validated_data['quantity']
        else:
            quantity = basket.get_product_line_count(product.id) + serializer.validated_data['quantity']
        basket.create_basket_lines(product.id, quantity)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        basketserializer = BasketSerializers(instance=serializer.validated_data['basket'])
        return Response(basketserializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AddShippingAPI(CreateAPIView):
    serializer_class = ShippingAddressSerializers
    permission_classes = [IsAuthenticated, IsPremiumTenant]



class GetUserShippingAPI(ListAPIView):
    serializer_class = ShippingAddressSerializers
    permission_classes = [IsAuthenticated, IsPremiumTenant]

    def get_queryset(self):
        return self.request.user.shipping_address.all()



class CreateOrderAPI(CreateAPIView):
    serializer_class = CreateOrderSerializers
    permission_classes = [IsAuthenticated, IsPremiumTenant]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        stripe_ser = StripetokenSerializers(data=request.data)
        stripe_ser.is_valid(raise_exception=True)
        serializer.is_valid(raise_exception=True)
        basket = serializer.validated_data['basket']
        number = settings.ORDER_NUMBERING_FROM + basket.id
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            charge = stripe.Charge.create(amount=int(basket.total()) * 100, currency='gbp',
                             source=stripe_ser.validated_data['stripe_token'],
                             description=f"charge for order number {number} tenant {request.tenant}")
        except Exception as e:
            return Response({"payment was not successful"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if charge.status == "succeeded":
                order = Order(basket=basket,
                                             user=request.user, number=str(number),
                                             total_incl_tax=basket.total(), transaction_id=charge.id,
                                             shipping_address=serializer.validated_data['shipping_address'])
                order.save()
                headers = self.get_success_headers(serializer.data)
                basket.status = basket.SUBMITTED
                basket.submitted_at = timezone.now()
                basket.save()
                data = OrderSerializers(instance=order).data
                return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"message": "payment was not successful"}, status=status.HTTP_400_BAD_REQUEST)


class GetUserOrdersAPI(ListAPIView):
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated, IsPremiumTenant]

    def get_queryset(self):
        return self.request.user.user_orders.all()


class SearchProductAPI(APIView):
    permission_classes = [AllowAny, IsPremiumTenant]

    def get(self, request):
        search = request.query_params.get("q")
        response = ProductDocument().response(search)
        hits = response.execute().hits

        # Serialize the hits data
        serialized_data = [
            {
                'id': hit.id,
                'title': hit.title,
                'description': hit.description,
                'tenant': hit.tenant,
                'get_image_url': hit.get_image_url,
                'brand': hit.brand,
                'category': hit.category,
                'price': hit.price,
                'is_available': hit.is_available,
                'search_keywords': hit.search_keywords,
                'score': hit.meta.score
            }
            for hit in hits
        ]
        return Response(serialized_data)











