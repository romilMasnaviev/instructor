from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'training-groups', TrainingGroupViewSet)
router.register(r'jump-groups', JumpGroupViewSet)
router.register(r'jump-requests', JumpRequestViewSet)
router.register(r'pre-jump-checks', PreJumpCheckViewSet)
router.register(r'jump-assignments', JumpAssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('pre-jump-checks/<int:group_id>/', PreJumpCheckViewSet.as_view({'get': 'list'})),
]