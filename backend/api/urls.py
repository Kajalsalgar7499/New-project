from django.urls import path

from . import views


urlpatterns = [
    path("health/", views.health),
    path("auth/register/", views.register),
    path("auth/login/", views.login),
    path("restaurants/", views.restaurant_list),
    path("restaurants/<str:restaurant_id>/", views.restaurant_detail),
    path("restaurants/<str:restaurant_id>/menu/", views.restaurant_menu),
    path("orders/", views.create_order),
    path("orders/<str:order_id>/", views.order_detail),
    path("orders/<str:order_id>/status/", views.update_order_status),
    path("admin/summary/", views.admin_summary),
]
