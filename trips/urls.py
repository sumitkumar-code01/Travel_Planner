from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# trips/urls.py
urlpatterns = [
    path('', views.intro_page, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.stylish_login, name='login'),
    # 'add/' ko badal kar 'add-trip/' kiya taaki 404 na aaye
    path('add-trip/', views.add_trip, name='add_trip'), 
    path('trip/<int:pk>/', views.trip_detail, name='trip_detail'),
    path('delete-trip/<int:id>/', views.delete_trip, name='delete_trip'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
    path('update-status/<int:it_id>/', views.update_status, name='update_status'),
]