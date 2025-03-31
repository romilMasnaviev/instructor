from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from instructors.urls import router

# Определяем настройки для Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Instructor API",
        default_version='v1',
        description="API для управления группами и прыжками парашютистов",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@instructorapi.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,  # Открываем доступ для всех пользователей
    permission_classes=[permissions.AllowAny],  # Разрешаем доступ анонимным пользователям
)

urlpatterns = [
    # Подключаем все URL-роуты из роутера
    path('', include(router.urls)),

    # Подключаем URL-ы из instructors.urls
    path('instructors/', include('instructors.urls')),  # Убедитесь, что путь в 'instructors.urls' правильный

    # Добавляем путь для Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
