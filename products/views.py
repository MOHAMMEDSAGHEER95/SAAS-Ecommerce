from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from tenant_schemas.utils import schema_context

from products.models import Products


class AddProductFromPublicSchema(View):

    @csrf_exempt
    def post(self, request):
        data = request.POST
        schema_name = data.get("schema_name")
        product = Products.objects.get(id=data.get("id"))
        with schema_context(schema_name):
            if Products.objects.filter(title=product.title).exists():
                return JsonResponse({"message": "Error"}, status=400)
            product_dictionary = {"title": product.title,
                                  "description": product.description, "url": product.image.url,
                                  "is_available": product.is_available, "price": product.price}
            Products.objects.create(**product_dictionary)
        return JsonResponse({"message": "Success"})
