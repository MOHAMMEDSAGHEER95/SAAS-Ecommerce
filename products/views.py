from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt


class AddProductFromPublicSchema(View):

    @csrf_exempt
    def post(self, request):
        return JsonResponse({"message": "Success"})
