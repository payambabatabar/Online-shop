from rest_framework import serializers
from. models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = serializers
    seller = serializers.ReadOnlyField(source="seller.username")

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['seller']

class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    product = serializers

    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ['user']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    product = serializers

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user']