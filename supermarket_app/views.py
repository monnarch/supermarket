from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from django.http import JsonResponse
import pandas as pd
from io import BytesIO
import openpyxl
from .models import Category, Product, Items, Shopcard, Customer
from .serializers import CategorySerializer, ProductSerializer, ItemsSerializer, ShopcardSerializer, CustomerSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ItemsViewSet(viewsets.ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer

class ShopcardViewSet(viewsets.ModelViewSet):
    queryset = Shopcard.objects.all()
    serializer_class = ShopcardSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class PurchaseHistoryView(generics.ListAPIView):
    serializer_class = ShopcardSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Shopcard.objects.filter(owner__id=customer_id)

class TotalPurchaseView(generics.RetrieveAPIView):

    def get(self, request, customer_id):
        total_purchase = Shopcard.objects.filter(owner__id=customer_id).aggregate(total_purchase=models.Sum('total_price'))
        if total_purchase['total_purchase'] and total_purchase['total_purchase'] > 10000000:
            return Response({'message': 'Total purchase is greater than 10,000,000 som'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Total purchase is not greater than 10,000,000 som'}, status=status.HTTP_200_OK)

class MarketTotalProductsView(generics.RetrieveAPIView):

    def get(self, request):
        total_products = Product.objects.count()
        return Response({'total_products': total_products}, status=status.HTTP_200_OK)

class ExpiredProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        from django.utils import timezone
        today = timezone.now().date()
        return Product.objects.filter(end_date__lt=today)

class BestSellingProductView(generics.RetrieveAPIView):

    def get(self, request):
        from django.db.models import Sum
        best_selling_product = Items.objects.values('product').annotate(total_sold=Sum('product__shopcard__total_price')).order_by('-total_sold').first()
        if best_selling_product:
            product = Product.objects.get(pk=best_selling_product['product'])
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No best selling product found'}, status=status.HTTP_200_OK)
