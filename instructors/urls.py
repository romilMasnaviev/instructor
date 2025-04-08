from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import InstructorTrainingGroupsAPIView

router = DefaultRouter()

# Регистрируем ViewSet для всех моделей
router.register(r'training-groups', views.TrainingGroupViewSet)
router.register(r'jump-groups', views.JumpGroupViewSet)
router.register(r'jump-requests', views.JumpRequestViewSet)
router.register(r'pre-jump-checks', views.PreJumpCheckViewSet)
router.register(r'jump-assignments', views.JumpAssignmentViewSet)
router.register(r'training-progress', views.TrainingProgressViewSet)
router.register(r'parachutists', views.ParachutistViewSet)
router.register(r'instructors', views.InstructorViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Все маршруты будут начинаться с /api/
    path('api/instructor/<int:instructor_id>/training-groups/', InstructorTrainingGroupsAPIView.as_view()),

]
