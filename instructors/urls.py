from django.urls import path
from instructors import views

urlpatterns = [
    path('instructors/', views.create_instructor, name='create_instructor'),  # Регистрирует нового инструктора
    path('instructors/<int:instructor_id>/', views.update_instructor, name='update_instructor'),  # Обновляет инструктора по ID
    path('instructors/<int:instructor_id>/qualification', views.update_instructor_qualification, name='update_instructor_qualification'),  # Обновляет квалификацию инструктора
]
