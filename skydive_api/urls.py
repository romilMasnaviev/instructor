from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Включаем маршруты для API, которые определены в app 'instructors'
    path('api/', include('instructors.urls')),  # Включаем URLs из приложения instructors
    path('api/', include('accounts.urls')),  # Включаем URLs из приложения accounts

]
