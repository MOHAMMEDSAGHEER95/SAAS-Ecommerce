from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from basket.models import Basket


# Create your views here.


class AddToBasket(View):

    def post(self, request):
        data = request.POST
        basket = Basket.objects.get(id=request.basket)
        lines = basket.create_basket_lines(data.get('id'), data.get('quantity'))
        return JsonResponse({"message": "Added to Cart", "count": lines})