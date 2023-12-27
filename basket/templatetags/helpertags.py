from django import template

from basket.models import Basket
from products.models import Products

register = template.Library()

@register.simple_tag
def check_product_exists(basket_id, product):
    return product.exists_in_basket(basket_id)

@register.simple_tag
def get_product_count(basket_id, product):
    basket = Basket.objects.get(id=basket_id)
    return basket.get_product_line_count(product.id)
