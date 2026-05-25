from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from trips import views


urlpatterns = [
    path('', views.home, name='landing'),
    path('register/', views.register_user, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-panel/login/', views.custom_admin_login, name='custom_admin_login'),
    path('admin-panel/dashboard/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    
    path('login/', views.stylish_login, name='login'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('about/', views.about_view, name='about_page'),
    path('add-trip/', views.add_trip, name='add_trip'), 
    path('trip/<int:pk>/', views.trip_detail, name='trip_detail'),
    path('delete-trip/<int:id>/', views.delete_trip, name='delete_trip'),
    path('update-status/<int:it_id>/', views.update_status, name='update_status'),
    
    # Use the custom functions for logic
    path('logout/', views.custom_logout, name='logout'),
    path('login-check/', views.login_redirect_handler, name='login_check'),
    path('package/', views.add_trip, name='package'),

    path('book-package/<str:place_name>/', views.book_package, name='book_package'),
    path('trip-details/', views.trip_details_view, name='trip_details_view'),
    path('generate-qr/', views.generate_payment_qr, name='generate_qr'),
    path('traveler-details/<str:place_name>/', views.traveler_details_view, name='traveler_details'),
    path('booking-confirmed/', views.booking_confirmed_view, name='booking_confirmed'),
]