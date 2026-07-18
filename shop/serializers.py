from rest_framework import serializers
from. models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    seller = serializers.ReadOnlyField(source="seller.username")

    def validate(self, attrs):
        if attrs['stock'] < 0:
            attrs['stock'] = 0
        if attrs['price'] < 0:
            attrs['price'] = 0
        return attrs

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['seller']

class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.username')
    product = ProductSerializer

    def validate(self, attrs):
        if attrs['quantity'] < 0:
            attrs['quantity'] = 1
        return attrs
        

    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ['user']

class OrderItemSerializer(serializers.ModelSerializer):
    
    def validate(self, attrs):
        if attrs['quantity'] < 0:
            attrs['quantity'] = 1
        return attrs
        
    
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