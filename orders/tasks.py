from celery import shared_task
from tenant_schemas.utils import schema_context

from customers.email import SendEmail
from orders.models import Order


@shared_task
def post_order_tasks(number, schema):
    print("inside celery")
    with schema_context(schema):
        order = Order.objects.get(number=number)
        lines = order.basket.lines.all()
        SendEmail().send_order_confirmation(order)
        for line in lines:
            product = line.product
            product.stock = product.stock - line.quantity
            if product.stock < 2:
                product.is_available = False
            product.save()
