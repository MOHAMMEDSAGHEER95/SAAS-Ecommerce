from django.utils.functional import SimpleLazyObject

from basket.models import Basket


class CustomBasketMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'basket' not in request.session:
            basket = Basket.create_basket()
            request.session['basket'] = SimpleLazyObject(basket.id)
        request.basket = request.session['basket']
        response = self.get_response(request)
        request.session['basket'] = request.basket
        return response
