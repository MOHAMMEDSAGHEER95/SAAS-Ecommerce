from django.core.signing import Signer
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from basket.models import Basket
from restapis.serializers import BasketSerializers


# Create your views here.



class BasketDetailAPIView(RetrieveAPIView):
    queryset = Basket
    serializer_class = BasketSerializers


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

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # if response.status_code == status.HTTP_200_OK:
        #     # user = self.user
        #     refresh = response.data['refresh']
        #     access = response.data['access']
        #     # response.data['user_id'] = user.id
        #     # response.data['username'] = user.username
        #     response.data['refresh_expires'] = RefreshToken(refresh)
        #     response.data['access_expires'] = RefreshToken(access)
        return response

