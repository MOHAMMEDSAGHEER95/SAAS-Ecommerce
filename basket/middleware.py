import time

from django.core.signing import Signer, BadSignature

from basket.models import Basket


from django.core.signing import Signer

class CustomBasketMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.tenant.schema_name != 'public':
            signer = Signer()
            basket_id = None

            if 'basket' in request.COOKIES:
                try:
                    unsigned_basket_id = signer.unsign_object(request.COOKIES['basket'])
                    basket_id = unsigned_basket_id.get("basket_id")
                    request.basket = basket_id
                except BadSignature:
                    # Handle the case where the cookie value is tampered or invalid
                    pass
            if 'basket' not in request.COOKIES:
                basket = Basket.create_basket(request.user)
                basket_id = basket.id
                request.basket = basket_id
            response = self.get_response(request)
            if 'basket' not in request.COOKIES:
                hash_value = signer.sign_object({"basket_id": basket_id})
                response.set_cookie("basket", hash_value, max_age=3600, secure=True, httponly=True)
                request.basket = basket_id
            return response
        else:
            response = self.get_response(request)
            return response
