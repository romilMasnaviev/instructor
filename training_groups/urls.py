from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainingGroupViewSet

router = DefaultRouter()
router.register(r'training-groups', TrainingGroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

