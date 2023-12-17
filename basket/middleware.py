
from basket.models import Basket


class CustomBasketMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.tenant.schema_name != 'public':
            if 'basket' in request.session and Basket.objects.filter(id=request.session['basket'], status=Basket.SUBMITTED):
                request.session.pop('basket')
            if 'basket' not in request.session:
                basket = Basket.create_basket(request.user)
                request.session['basket'] = basket.id
            request.basket = request.session['basket']
            response = self.get_response(request)
            request.session['basket'] = request.basket
            return response
        else:
            response = self.get_response(request)
            return response
