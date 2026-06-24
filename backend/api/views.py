from uuid import uuid4

from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .db import get_database, mongo_available
from .repositories import OrderRepository, RestaurantRepository
from .serializers import CreateOrderSerializer, LoginSerializer, OrderStatusSerializer, RegisterSerializer


restaurants = RestaurantRepository()
orders = OrderRepository()


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "mongo_connected": mongo_available()})


@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    user = {
        "id": f"user-{uuid4().hex[:10]}",
        "name": data["name"],
        "email": data["email"],
        "password": make_password(data["password"]),
        "role": data["role"],
    }

    if mongo_available():
        users = get_database()["users"]
        if users.find_one({"email": user["email"]}):
            return Response({"detail": "Email already registered."}, status=status.HTTP_409_CONFLICT)
        users.insert_one(user)

    return Response({"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    if mongo_available():
        user = get_database()["users"].find_one({"email": data["email"]})
        if user and check_password(data["password"], user["password"]):
            return Response({"token": f"demo-token-{uuid4().hex}", "name": user["name"], "role": user.get("role", "customer")})

    return Response({"detail": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def restaurant_list(request):
    return Response(restaurants.list(search=request.query_params.get("search"), cuisine=request.query_params.get("cuisine")))


@api_view(["GET"])
def restaurant_detail(request, restaurant_id):
    restaurant = restaurants.get(restaurant_id)
    if not restaurant:
        return Response({"detail": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(restaurant)


@api_view(["GET"])
def restaurant_menu(request, restaurant_id):
    restaurant = restaurants.get(restaurant_id)
    if not restaurant:
        return Response({"detail": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(restaurant.get("menu", []))


@api_view(["POST"])
def create_order(request):
    serializer = CreateOrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(orders.create(serializer.validated_data), status=status.HTTP_201_CREATED)


@api_view(["GET"])
def order_detail(request, order_id):
    order = orders.get(order_id)
    if not order:
        return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(order)


@api_view(["PATCH"])
def update_order_status(request, order_id):
    serializer = OrderStatusSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    order = orders.update_status(order_id, serializer.validated_data["status"])
    if not order:
        return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(order)


@api_view(["GET"])
def admin_summary(request):
    restaurant_count = len(restaurants.list())
    order_list = orders.list()
    revenue = sum(order.get("total", 0) for order in order_list)
    return Response(
        {
            "restaurants": restaurant_count,
            "orders": len(order_list),
            "revenue": revenue,
            "latest_orders": order_list[:5],
        }
    )
