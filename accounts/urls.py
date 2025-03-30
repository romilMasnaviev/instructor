from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Endpoint for registering a new account
    path('user/<int:user_id>/', views.get_user, name='get_user'),  # Endpoint to get user details
    path('user/<int:user_id>/update/', views.update_user, name='update_user'),  # Endpoint for updating user details
]