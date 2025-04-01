from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import TrainingGroup, JumpGroup, JumpRequest, PreJumpCheck, JumpAssignment, TrainingGroupParachutist, \
    Parachutist, Instructor
from .serializers import TrainingGroupSerializer, JumpGroupSerializer, JumpRequestSerializer, PreJumpCheckSerializer, \
    JumpAssignmentSerializer, TrainingGroupParachutistSerializer, ParachutistSerializer, InstructorSerializer


# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import TrainingGroup
from .serializers import TrainingGroupSerializer

class TrainingGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = TrainingGroup.objects.all()
    serializer_class = TrainingGroupSerializer

    class TrainingGroupViewSet(viewsets.ModelViewSet):
        permission_classes = [AllowAny]
        queryset = TrainingGroup.objects.all()
        serializer_class = TrainingGroupSerializer

        @action(detail=True, methods=['put'], url_path='status')
        def update_status(self, request, pk=None):
            """
            Кастомный эндпоинт для обновления статуса учебной группы.
            Путь: /training-groups/{group_id}/status/
            Позволяет обновить статус учебной группы (Создана, в процессе, завершена).
            """
            # TODO : добавить проверку что инструктор,
            #  который меняет это является инструктором данной группы
            group = self.get_object()  # Получаем группу по pk
            new_status = request.data.get('status')

            # Проверяем, что статус передан и является одним из разрешенных
            if new_status not in dict(TrainingGroup.STATUS_CHOICES):
                return Response({"error": "Неверный статус."}, status=status.HTTP_400_BAD_REQUEST)

            # Обновляем статус
            group.status = new_status
            group.save()  # Сохраняем изменения

            return Response(TrainingGroupSerializer(group).data, status=status.HTTP_200_OK)

# 2. JumpGroupViewSet для прыжковых групп
class JumpGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = JumpGroup.objects.all()
    serializer_class = JumpGroupSerializer


# 3. JumpRequestViewSet для заявок на прыжок
class JumpRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = JumpRequest.objects.all()
    serializer_class = JumpRequestSerializer


# 4. PreJumpCheckViewSet для проверок перед прыжком
class PreJumpCheckViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = PreJumpCheck.objects.all()
    serializer_class = PreJumpCheckSerializer


# 5. JumpAssignmentViewSet для заданий
class JumpAssignmentViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = JumpAssignment.objects.all()
    serializer_class = JumpAssignmentSerializer


# 6. TrainingProgressViewSet для отслеживания обучения
class TrainingProgressViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = TrainingGroupParachutist.objects.all()
    serializer_class = TrainingGroupParachutistSerializer

    @action(detail=True, methods=['patch'], url_path='progress')
    def update_progress(self, request, pk=None):
        """
        Кастомный эндпоинт для обновления прогресса парашютиста в учебной группе.
        Путь: /training-groups/{group_id}/parachutists/{parachutist_id}/progress/
        Позволяет обновить статусы теории, практики и зачета.
        """
        progress = self.get_object()
        data = request.data

        allowed_fields = {'theory_passed', 'practice_passed', 'exam_passed'}
        received_fields = set(data.keys())

        invalid_fields = received_fields - allowed_fields
        if invalid_fields:
            return Response({"error": f"Неверные поля: {', '.join(invalid_fields)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        for field in received_fields:
            setattr(progress, field, data[field])

        progress.save()
        return Response(TrainingGroupParachutistSerializer(progress).data, status=status.HTTP_200_OK)

# 7. ParachutistViewSet для парашютистов
class ParachutistViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Parachutist.objects.all()
    serializer_class = ParachutistSerializer


# 8. InstructorViewSet для инструкторов
class InstructorViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
