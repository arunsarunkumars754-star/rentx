from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    # Static Assets & Fallbacks (Eliminates terminal 404s)
    path('favicon.ico', views.favicon_view, name='favicon'),
    path('api/chatbot/', views.chatbot_fallback, name='chatbot_fallback'),
    
    # Common navigation aliases
    path('customer-dashboard/', lambda r: redirect('my_bookings')),
    path('customer_dashboard/', lambda r: redirect('my_bookings')),
    path('vehicle-list/', lambda r: redirect('vehicles_catalog')),
    path('vehicle_list/', lambda r: redirect('vehicles_catalog')),

    # Public Client Pages
    path('', views.home, name='home'),
    path('vehicles/', views.vehicles_catalog, name='vehicles_catalog'),
    path('vehicles/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail'),
    path('book/<int:vehicle_id>/', views.book_vehicle, name='book_vehicle'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin Portal & Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/vehicle/add/', views.add_vehicle, name='add_vehicle'),
    path('dashboard/vehicle/edit/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('dashboard/vehicle/delete/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('dashboard/category/add/', views.add_category, name='add_category'),
    path('dashboard/category/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('dashboard/category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('dashboard/customer/add/', views.add_customer, name='add_customer'),
    path('dashboard/customer/edit/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('dashboard/customer/delete/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    path('dashboard/booking/add/', views.add_booking, name='add_booking'),
    path('dashboard/payment/add/', views.add_payment, name='add_payment'),
    path('dashboard/report/generate/', views.generate_report, name='generate_report'),
]

