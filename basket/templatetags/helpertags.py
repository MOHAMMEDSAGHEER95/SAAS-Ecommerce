from django import template

from basket.models import Basket
from products.models import Products, Category

register = template.Library()

@register.simple_tag
def check_product_exists(basket_id, product_id):
    product = Products.objects.get(id=product_id)
    return product.exists_in_basket(basket_id)

@register.simple_tag
def get_product_count(basket_id, product):
    basket = Basket.objects.get(id=basket_id)
    return basket.get_product_line_count(product.id)


@register.simple_tag
def get_categories():
    return Category.objects.all()
