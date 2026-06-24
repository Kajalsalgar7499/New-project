from datetime import datetime, timezone
from uuid import uuid4

from bson import ObjectId

from .db import get_database, mongo_available
from .sample_data import ORDERS, RESTAURANTS


def _clean_id(document):
    if not document:
        return document
    document = dict(document)
    if "_id" in document:
        document["id"] = str(document.pop("_id"))
    return document


class RestaurantRepository:
    collection_name = "restaurants"

    def list(self, search=None, cuisine=None):
        if not mongo_available():
            restaurants = RESTAURANTS
        else:
            query = {}
            if search:
                query["name"] = {"$regex": search, "$options": "i"}
            if cuisine:
                query["cuisine"] = {"$regex": f"^{cuisine}$", "$options": "i"}
            restaurants = [_clean_id(row) for row in get_database()[self.collection_name].find(query)]

        return [
            restaurant
            for restaurant in restaurants
            if (not search or search.lower() in restaurant["name"].lower())
            and (not cuisine or cuisine.lower() == restaurant["cuisine"].lower())
        ]

    def get(self, restaurant_id):
        if not mongo_available():
            return next((item for item in RESTAURANTS if item["id"] == restaurant_id), None)

        collection = get_database()[self.collection_name]
        query = {"_id": ObjectId(restaurant_id)} if ObjectId.is_valid(restaurant_id) else {"id": restaurant_id}
        return _clean_id(collection.find_one(query))


class OrderRepository:
    collection_name = "orders"

    def create(self, payload):
        order = {
            "id": f"order-{uuid4().hex[:10]}",
            "customer": payload["customer"],
            "restaurant_id": payload["restaurant_id"],
            "items": payload["items"],
            "total": sum(item["price"] * item["quantity"] for item in payload["items"]),
            "payment_method": payload.get("payment_method", "cash"),
            "payment_status": "paid" if payload.get("payment_method") != "cash" else "pending",
            "status": "received",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        if not mongo_available():
            ORDERS.append(order)
            return order

        get_database()[self.collection_name].insert_one(order)
        return order

    def get(self, order_id):
        if not mongo_available():
            return next((item for item in ORDERS if item["id"] == order_id), None)

        order = get_database()[self.collection_name].find_one({"id": order_id})
        return _clean_id(order)

    def update_status(self, order_id, status):
        if not mongo_available():
            order = self.get(order_id)
            if order:
                order["status"] = status
            return order

        collection = get_database()[self.collection_name]
        collection.update_one({"id": order_id}, {"$set": {"status": status}})
        return _clean_id(collection.find_one({"id": order_id}))

    def list(self):
        if not mongo_available():
            return ORDERS
        return [_clean_id(row) for row in get_database()[self.collection_name].find({}).sort("created_at", -1)]
