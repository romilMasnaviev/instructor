from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParachutistViewSet

router = DefaultRouter()
router.register(r'parachutists', ParachutistViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

