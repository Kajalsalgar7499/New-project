from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)
    role = serializers.ChoiceField(choices=["customer", "admin"], default="customer")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class CustomerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    phone = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=250)


class OrderItemSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=80)
    name = serializers.CharField(max_length=120)
    price = serializers.FloatField(min_value=0)
    quantity = serializers.IntegerField(min_value=1)


class CreateOrderSerializer(serializers.Serializer):
    customer = CustomerSerializer()
    restaurant_id = serializers.CharField(max_length=80)
    items = OrderItemSerializer(many=True, allow_empty=False)
    payment_method = serializers.ChoiceField(choices=["cash", "card", "upi", "wallet"], default="cash")


class OrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["received", "preparing", "out_for_delivery", "delivered", "cancelled"])
