# views.py
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from .models import JumpRequest, PreJumpCheck, JumpAssignment, TrainingGroupParachutist, \
    Parachutist, Instructor
from .models import TrainingGroup
from .serializers import JumpRequestSerializer, PreJumpCheckSerializer, \
    JumpAssignmentSerializer, TrainingGroupParachutistSerializer, ParachutistSerializer, InstructorSerializer
from .serializers import TrainingGroupSerializer


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
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import JumpGroup
from .serializers import JumpGroupSerializer


class JumpGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = JumpGroup.objects.all()
    serializer_class = JumpGroupSerializer

    @action(detail=False, methods=['get'], url_path='instructors/(?P<instructor_id>\d+)/jump-groups')
    def get_jump_groups_by_instructor(self, request, instructor_id=None):
        """
        Кастомный эндпоинт для получения списка прыжковых групп данного инструктора.
        Путь: /instructors/{instructor_id}/jump-groups/
        Возвращает список групп, где указанный инструктор является либо instructor_air, либо instructor_ground.
        """

        # Получаем все группы, где инструктор является либо air, либо ground инструктором
        jump_groups = JumpGroup.objects.filter(
            Q(instructor_air__id=instructor_id) | Q(instructor_ground__id=instructor_id)
        )

        # Если группы не найдены, возвращаем ошибку
        if not jump_groups.exists():
            return Response({"error": "У инструктора нет прыжковых групп."}, status=status.HTTP_404_NOT_FOUND)

        # Возвращаем сериализованные данные
        return Response(JumpGroupSerializer(jump_groups, many=True).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], url_path='status')
    def update_status(self, request, pk=None):
        """
        Эндпоинт для изменения статуса прыжковой группы.
        Путь: /jump-groups/{group_id}/status/
        Позволяет обновить статус прыжковой группы на 'Completed' (Завершена), 'Planned' (Запланирован) или 'Cancelled' (Отменена).
        """
        # TODO : добавить проверку что инструктор,
        #  который меняет это является инструктором данной группы (либо земным,
        #  либо воздушным)
        try:
            # Получаем группу по pk (параметр id из URL)
            jump_group = JumpGroup.objects.get(id=pk)
        except JumpGroup.DoesNotExist:
            return Response({"error": "Прыжковая группа не найдена."}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, что новый статус передан в запросе
        status_value = request.data.get('status', None)
        if not status_value:
            return Response({"error": "Не указан новый статус."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, что статус имеет допустимое значение
        if status_value not in ['Planned', 'Completed', 'Cancelled']:
            return Response({"error": "Неверный статус."}, status=status.HTTP_400_BAD_REQUEST)

        # Обновляем статус группы
        jump_group.status = status_value
        jump_group.save()

        # Возвращаем обновленную группу
        return Response(JumpGroupSerializer(jump_group).data, status=status.HTTP_200_OK)

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

    @action(detail=True, methods=['put'], url_path='check')
    def update_check(self, request, check_id=None):
        """
        Кастомный эндпоинт для обновления проверки перед прыжком для конкретного парашютиста.
        Путь: /pre-jump-checks/{check_id}/
        Позволяет обновить информацию о допусках для прыжка (теория, практика, медицинская сертификация, проверка снаряжения).
        """

        try:
            # Получаем проверку по check_id
            pre_jump_check = PreJumpCheck.objects.get(pre_jump_check_id=check_id)
        except PreJumpCheck.DoesNotExist:
            return Response({"error": "Проверка не найдена."}, status=status.HTTP_404_NOT_FOUND)

        # Получаем ID парашютиста из проверки
        parachutist = pre_jump_check.parachutist_id
        # TODO : Переделать метод на GET, убрать обновление полей theory_passed и
        #  practice_passed. Остальные поля (medical_certified, equipment_checked)
        #  запрашивать из других модулей. Этот метод по сути будет обновлять данные,
        #  взятые из других модулей
        # Обновляем поля проверки
        pre_jump_check.theory_passed = request.data.get('theory_passed', pre_jump_check.theory_passed)
        pre_jump_check.practice_passed = request.data.get('practice_passed', pre_jump_check.practice_passed)
        pre_jump_check.medical_certified = request.data.get('medical_certified', pre_jump_check.medical_certified)
        pre_jump_check.equipment_checked = request.data.get('equipment_checked', pre_jump_check.equipment_checked)

        # Сохраняем изменения
        pre_jump_check.save()

        # Возвращаем обновленную информацию
        return Response(PreJumpCheckSerializer(pre_jump_check).data, status=status.HTTP_200_OK)


# 5. JumpAssignmentViewSet для заданий
class JumpAssignmentViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = JumpAssignment.objects.all()
    serializer_class = JumpAssignmentSerializer

    @action(detail=True, methods=['put'], url_path='update-status')
    def update_assignment(self, request, assignment_id=None):
        """
        Кастомный эндпоинт для обновления статуса полетного задания парашютиста.
        Путь: /jump-assignments/{assignment_id}/
        Позволяет обновить информацию о статусе выполнения задания и оценке.
        """
        try:
            # Получаем задание по assignment_id
            assignment = JumpAssignment.objects.get(id=assignment_id)
        except JumpAssignment.DoesNotExist:
            return Response({"error": "Задание не найдено."}, status=status.HTTP_404_NOT_FOUND)

        # Обновляем поля в задании
        completed = request.data.get('completed', None)
        score = request.data.get('score', None)

        if completed is not None:
            assignment.completed = completed  # Обновляем статус выполнения задания

        if score is not None:
            if score not in [0, 1, 2, 3, 4, 5]:
                return Response({"error": "Оценка должна быть от 0 до 5."}, status=status.HTTP_400_BAD_REQUEST)
            assignment.score = score  # Обновляем оценку задания

        # Сохраняем изменения
        assignment.save()

        # Возвращаем обновленную информацию о задании
        return Response(JumpAssignmentSerializer(assignment).data, status=status.HTTP_200_OK)


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
        # TODO : добавить проверку что инструктор,
        #  который меняет это является инструктором данного парашютиста
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
