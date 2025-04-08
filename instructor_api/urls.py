from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from instructors import views  # Импортируйте ваши ViewSet'ы
from instructors.views import UpdateCheckpointsAPIView, StartTrainingAPIView, InstructorTrainingGroupsAPIView, \
    EndTrainingAPIView

# Определение Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Instructor API",
        default_version='v1',
        description="API для управления группами и прыжками парашютистов",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@instructorapi.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

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
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('api/instructor/<int:instructor_id>/training-groups/', InstructorTrainingGroupsAPIView.as_view(),
         name='instructor-training-groups'),
    path('api/instructor/<int:instructor_id>/training-group/<int:group_id>/start/', StartTrainingAPIView.as_view(),
         name='start-training'),
    path(
        'api/instructor/<int:instructor_id>/training-group/<int:group_id>/parachutist/<int:parachutist_id>/update-checkpoints/',
        UpdateCheckpointsAPIView.as_view(), name='update-checkpoints'),
    path('api/instructor/<int:instructor_id>/training-group/<int:group_id>/end/', EndTrainingAPIView.as_view(),
         name='end-training'),

]
