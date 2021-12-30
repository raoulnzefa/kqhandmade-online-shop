
import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import serializers, status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():   
        stripe.api_key = settings.STRIPE_SECRET_KEY
        print(stripe.api_key)
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
        print(paid_amount)

        try:
            print('initiate stripe')
            charge = stripe.Charge.create(
                amount=int(paid_amount * 100), 
                currency='CAD',
                description='Charge from KQ HandMade', 
                source=serializer.validated_data['stripe_token'] 
            )
            print('stripe charged')

            serializer.save(user=request.user, paid_amount=paid_amount)
            print('stripe processed')

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)