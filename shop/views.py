from django.shortcuts import render, redirect
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .permissions import IsSellerOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
# Create your views here.

def Home(request):
    return render(request,'home.html')

def go_home(request):
    return redirect('/api/home/')


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'seller', 'stock']
    search_fields = ['title', 'description']

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"message":"باید وارد شوید"}, status = 401)
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"message":"باید وارد شوید"}, status = 401)
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(seller = self.request.user)

class CartViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["POST"])
    def add(self, request):
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "کالا پیدا نشد"}, status=400)
        
        if product.stock < quantity:
            return Response({"message": "موجودی کافی نیست"})
        item, created = CartItem.objects.get_or_create(
            user = request.user,
            product = product
        )
        item.quantity += quantity
        product.stock - quantity
        item.save()
        product.save()

        return Response({"message": "به سبد خرید اضافه شد"})

@api_view(["GET"])
def view_cart(request):
    items = CartItem.objects.filter(user=request.user)
    serializer = CartItemSerializer(items, many=True)
    return Response(serializer.data)

class CreateOrderViewset(viewsets.ViewSet):
    def create(self, request):
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items.exists:
            return Response({"message": "سبد خرید خالی می باشد"}, status=400)

        total = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user, total_price=total)

        for item in cart_items:
            OrderItem.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                price = item.product.price
            )
        
        cart_items.delete()

        return Response({"message":"سفارش ثبت شد"}, status=200)

@api_view(["GET"])
def seller_order(request):
    products = Product.objects.filter(seller = request.user)
    orders = OrderItem.objects.filter(product__in=products)
    serializer = OrderItemSerializer(orders, many=True)
    return Response(serializer.data)

class review(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"message": "باید وارد شوید"}, status=401)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"message": "باید وارد شوید"}, status=401)
        return super().destroy(request, *args, **kwargs)
    
class ProductReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer()

    def get_queryset(self):
        product_id = self.kwargs("pk")
        return Review.objects.filter(product_id=product_id)