from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .permissions import IsSellerOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.
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

@api_view(["POST"])
def add_to_cart(request):
    if not request.user.is_authenticated:
        return Response({"message": "باید وارد شوید"})
    product_id = request.data.get("product")
    quantity = int(request.data.get("quantity", 1))

    try:
        product = product.objects.get(id=product_id)
    except product.DoesNotExist:
        return Response({"message": "کالا پیدا نشد"})
    
    item = CartItem.objects.filter(user=request.user, product=product)

    if item is None:
        CartItem.objects.create(user=request.user, product=product)

    if item.quantity + quantity > product.stock:
        return Response({"message": "موجودی کافی نیست"}, status=400)
    item.quantity += quantity
    item.save()
    return Response({"message": "کالا به سبد خرید اضافه شد"}, status=200)

@api_view(["GET"])
def view_cart(request):
    items = CartItem.objects.filter(user=request.user)
    serializer = CartItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def create_order(request):
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