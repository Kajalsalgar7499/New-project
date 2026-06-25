from uuid import uuid4

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from api.db import mongo_available
from api.repositories import OrderRepository, RestaurantRepository, UserRepository


api = Blueprint("api", __name__)
restaurants = RestaurantRepository()
orders = OrderRepository()
users = UserRepository()

ORDER_STATUSES = {"received", "preparing", "out_for_delivery", "delivered", "cancelled"}


def _json_error(message, status_code):
    return jsonify({"detail": message}), status_code


def _payload():
    return request.get_json(silent=True) or {}


def _validate_customer(customer):
    if not isinstance(customer, dict):
        return "Customer details are required."
    for field in ("name", "phone", "address"):
        if not str(customer.get(field, "")).strip():
            return f"Customer {field} is required."
    return None


def _validate_items(items):
    if not isinstance(items, list) or not items:
        return "At least one cart item is required."
    for item in items:
        if not isinstance(item, dict):
            return "Each cart item must be an object."
        if not item.get("id") or not item.get("name"):
            return "Each cart item needs an id and name."
        try:
            price = float(item.get("price"))
            quantity = int(item.get("quantity"))
        except (TypeError, ValueError):
            return "Each cart item needs a valid price and quantity."
        if price <= 0 or quantity <= 0:
            return "Cart item prices and quantities must be greater than zero."
    return None


@api.get("/health/")
def health():
    return jsonify({"status": "ok", "mongo_connected": mongo_available(), "service": "FoodExpress API"})


@api.post("/seed/")
def seed_data():
    return jsonify(restaurants.seed())


@api.post("/auth/register/")
def register():
    data = _payload()
    for field in ("name", "email", "password"):
        if not str(data.get(field, "")).strip():
            return _json_error(f"{field.title()} is required.", 400)

    user = {
        "id": f"user-{uuid4().hex[:10]}",
        "name": data["name"].strip(),
        "email": data["email"].strip().lower(),
        "password": generate_password_hash(data["password"]),
        "role": data.get("role", "customer"),
    }
    created = users.create(user)
    if created is None:
        return _json_error("Email already registered.", 409)

    return jsonify({"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]}), 201


@api.post("/auth/login/")
def login():
    data = _payload()
    if not data.get("email") or not data.get("password"):
        return _json_error("Email and password are required.", 400)

    user = users.find_by_email(data["email"].strip().lower())
    if user and check_password_hash(user["password"], data["password"]):
        return jsonify({"token": f"demo-token-{uuid4().hex}", "name": user["name"], "role": user.get("role", "customer")})

    return _json_error("Invalid email or password.", 401)


@api.get("/restaurants/")
def restaurant_list():
    return jsonify(restaurants.list(search=request.args.get("search"), cuisine=request.args.get("cuisine")))


@api.get("/restaurants/<restaurant_id>/")
def restaurant_detail(restaurant_id):
    restaurant = restaurants.get(restaurant_id)
    if not restaurant:
        return _json_error("Restaurant not found.", 404)
    return jsonify(restaurant)


@api.get("/restaurants/<restaurant_id>/menu/")
def restaurant_menu(restaurant_id):
    restaurant = restaurants.get(restaurant_id)
    if not restaurant:
        return _json_error("Restaurant not found.", 404)
    return jsonify(restaurant.get("menu", []))


@api.post("/orders/")
def create_order():
    data = _payload()
    customer_error = _validate_customer(data.get("customer"))
    if customer_error:
        return _json_error(customer_error, 400)
    item_error = _validate_items(data.get("items"))
    if item_error:
        return _json_error(item_error, 400)
    if not data.get("restaurant_id"):
        return _json_error("Restaurant id is required.", 400)

    return jsonify(orders.create(data)), 201


@api.get("/orders/<order_id>/")
def order_detail(order_id):
    order = orders.get(order_id)
    if not order:
        return _json_error("Order not found.", 404)
    return jsonify(order)


@api.patch("/orders/<order_id>/status/")
def update_order_status(order_id):
    status = _payload().get("status")
    if status not in ORDER_STATUSES:
        return _json_error("Status must be one of: received, preparing, out_for_delivery, delivered, cancelled.", 400)

    order = orders.update_status(order_id, status)
    if not order:
        return _json_error("Order not found.", 404)
    return jsonify(order)


@api.get("/admin/summary/")
def admin_summary():
    order_list = orders.list()
    return jsonify(
        {
            "restaurants": len(restaurants.list()),
            "orders": len(order_list),
            "revenue": sum(order.get("total", 0) for order in order_list),
            "latest_orders": order_list[:5],
        }
    )
