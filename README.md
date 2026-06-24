# Online Food Ordering System

A full-stack starter project based on the synopsis:

- Frontend: React.js
- Backend: Django and Django REST Framework
- Database: MongoDB

The application lets customers browse restaurants, view menus, add food to a cart, checkout, and track orders. It also includes starter admin APIs for restaurant, menu, and order management.

## Project Structure

```text
backend/
  api/
    db.py
    repositories.py
    serializers.py
    urls.py
    views.py
  food_ordering/
    settings.py
    urls.py
  manage.py
  requirements.txt
frontend/
  src/
    components/
    data/
    services/
    App.jsx
    main.jsx
  package.json
  index.html
```

## Backend Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py runserver
```

By default, the backend uses this MongoDB URL:

```text
mongodb://localhost:27017/food_ordering
```

You can change it with:

```powershell
$env:MONGODB_URI="mongodb://localhost:27017/food_ordering"
```

## Frontend Setup

```powershell
cd frontend
npm install
npm run dev
```

The frontend expects the backend at:

```text
http://localhost:8000/api
```

You can change it by creating `frontend/.env`:

```text
VITE_API_BASE_URL=http://localhost:8000/api
```

## Main Features

- User registration and login API
- Restaurant listing, searching, and filtering
- Dynamic menu display
- Add to cart and checkout
- Order creation and tracking
- Payment record placeholder
- Admin dashboard data endpoints
- Responsive React interface

## API Endpoints

```text
GET    /api/health/
POST   /api/auth/register/
POST   /api/auth/login/
GET    /api/restaurants/
GET    /api/restaurants/<restaurant_id>/
GET    /api/restaurants/<restaurant_id>/menu/
POST   /api/orders/
GET    /api/orders/<order_id>/
PATCH  /api/orders/<order_id>/status/
GET    /api/admin/summary/
```

## Notes

This is a clean project starter, not a production deployment. Before production use, add stronger authentication, real payment gateway integration, order permissions, validation hardening, and map-based delivery tracking.
