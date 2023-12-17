from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from basket.models import Basket


# Create your views here.


class AddToBasket(View):

    def post(self, request):
        data = request.POST
        basket = Basket.objects.get(id=request.basket)
        lines = basket.create_basket_lines(data.get('id'), data.get('quantity'))
        return JsonResponse({"message": "Added to Cart", "count": lines})

class BasketDetailView(DetailView):
    model = Basket
    template_name = 'basket/basket.html'

    def get_object(self, queryset=None):
        return Basket.objects.get(id=self.request.basket)