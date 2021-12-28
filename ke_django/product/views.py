from django.db.models import Q
from django.http import Http404
from rest_framework import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view



from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer

class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializers = ProductSerializer(products, many=True)
        return Response(serializers.data)

class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
        
    def get(self, request, category_slug, product_slug, format=None):
         product = self.get_object(category_slug, product_slug)
         serializers = ProductSerializer(product)
         return Response(serializers.data)

class CategoryDetail(APIView):

    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
         category = self.get_object(category_slug)
         serializers = CategorySerializer(category)
         return Response(serializers.data)

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializers = ProductSerializer(products, many=True)
        return Response(serializers.data)
    else:
        return Response({"products": []})