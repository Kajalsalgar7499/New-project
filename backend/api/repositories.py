from datetime import datetime, timezone
from uuid import uuid4

from bson import ObjectId

from api.db import get_database, mongo_available
from api.sample_data import ORDERS, RESTAURANTS


def _clean_id(document):
    if not document:
        return document
    cleaned = dict(document)
    if "_id" in cleaned:
        cleaned["id"] = str(cleaned.pop("_id"))
    return cleaned


def _restaurant_matches(restaurant, search=None, cuisine=None):
    search_text = f"{restaurant.get('name', '')} {restaurant.get('cuisine', '')}".lower()
    return (
        (not search or search.lower() in search_text)
        and (not cuisine or cuisine.lower() == restaurant.get("cuisine", "").lower())
    )


class UserRepository:
    collection_name = "users"

    def create(self, user):
        if mongo_available():
            collection = get_database()[self.collection_name]
            if collection.find_one({"email": user["email"]}):
                return None
            collection.insert_one(user)
        return user

    def find_by_email(self, email):
        if not mongo_available():
            return None
        return _clean_id(get_database()[self.collection_name].find_one({"email": email}))


class RestaurantRepository:
    collection_name = "restaurants"

    def list(self, search=None, cuisine=None):
        if not mongo_available():
            restaurants = RESTAURANTS
        else:
            query = {}
            if search:
                query["$or"] = [
                    {"name": {"$regex": search, "$options": "i"}},
                    {"cuisine": {"$regex": search, "$options": "i"}},
                ]
            if cuisine:
                query["cuisine"] = {"$regex": f"^{cuisine}$", "$options": "i"}
            restaurants = [_clean_id(row) for row in get_database()[self.collection_name].find(query)]
            if not restaurants and not search and not cuisine:
                restaurants = RESTAURANTS

        return [restaurant for restaurant in restaurants if _restaurant_matches(restaurant, search, cuisine)]

    def get(self, restaurant_id):
        if not mongo_available():
            return next((item for item in RESTAURANTS if item["id"] == restaurant_id), None)

        collection = get_database()[self.collection_name]
        query = {"_id": ObjectId(restaurant_id)} if ObjectId.is_valid(restaurant_id) else {"id": restaurant_id}
        return _clean_id(collection.find_one(query))

    def seed(self):
        if not mongo_available():
            return {"inserted": 0, "message": "MongoDB is not connected; using demo data."}

        collection = get_database()[self.collection_name]
        inserted = 0
        for restaurant in RESTAURANTS:
            if not collection.find_one({"id": restaurant["id"]}):
                collection.insert_one(dict(restaurant))
                inserted += 1
        return {"inserted": inserted, "message": "Restaurant sample data is ready."}


class OrderRepository:
    collection_name = "orders"

    def create(self, payload):
        order = {
            "id": f"order-{uuid4().hex[:10]}",
            "customer": payload["customer"],
            "restaurant_id": payload["restaurant_id"],
            "items": payload["items"],
            "total": sum(float(item["price"]) * int(item["quantity"]) for item in payload["items"]),
            "payment_method": payload.get("payment_method", "cash"),
            "payment_status": "pending" if payload.get("payment_method") == "cash" else "paid",
            "status": "received",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        if not mongo_available():
            ORDERS.insert(0, order)
            return order

        get_database()[self.collection_name].insert_one(dict(order))
        return order

    def get(self, order_id):
        if not mongo_available():
            return next((item for item in ORDERS if item["id"] == order_id), None)

        return _clean_id(get_database()[self.collection_name].find_one({"id": order_id}))

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
