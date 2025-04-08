# views.py
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import JumpGroup
from .models import JumpRequest, PreJumpCheck, JumpAssignment, TrainingGroupParachutist, \
    Parachutist, Instructor
from .models import TrainingGroup
from .serializers import JumpGroupSerializer
from .serializers import JumpRequestSerializer, PreJumpCheckSerializer, \
    JumpAssignmentSerializer, TrainingGroupParachutistSerializer, ParachutistSerializer, InstructorSerializer
from .serializers import TrainingGroupSerializer


class InstructorTrainingGroupsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, instructor_id):
        # Получаем инструктора по ID
        instructor = get_object_or_404(Instructor, pk=instructor_id)

        # Получаем все группы, связанные с этим инструктором
        groups = TrainingGroup.objects.filter(instructor=instructor)

        # Подготовим список групп с парашютистами
        groups_data = []
        for group in groups:
            # Получаем парашютистов, связанных с этой группой
            parachutists = TrainingGroupParachutist.objects.filter(group=group)
            parachutist_data = TrainingGroupParachutistSerializer(parachutists, many=True).data

            group_data = TrainingGroupSerializer(group).data
            group_data['parachutists'] = parachutist_data  # Включаем парашютистов в данные группы
            groups_data.append(group_data)

        return Response(groups_data, status=status.HTTP_200_OK)


class StartTrainingAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, instructor_id, group_id):
        # Получаем группу и проверяем, что инструктор совпадает
        group = get_object_or_404(TrainingGroup, pk=group_id, instructor_id=instructor_id)

        # Проверка, что группа в статусе "created"
        if group.status != 'created':
            return Response({
                "status": "error",
                "message": "Группа уже не в статусе 'Создана', нельзя начать обучение."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Меняем статус на "in_progress"
        group.status = 'in_progress'
        group.save()

        return Response({
            "status": "ok",
            "group_status": group.status
        }, status=status.HTTP_200_OK)


class UpdateCheckpointsAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, instructor_id, group_id, parachutist_id):
        # Получаем группу и парашютиста
        group = get_object_or_404(TrainingGroup, pk=group_id)
        parachutist = get_object_or_404(Parachutist, pk=parachutist_id)

        # Проверка, что статус группы "in_progress"
        if group.status != 'in_progress':
            return Response(
                {"status": "error", "message": "Группа не в процессе."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверка, что инструктор назначен на эту группу
        if group.instructor.instructor_id != int(instructor_id):
            return Response(
                {"status": "error", "message": "Инструктор не назначен на эту группу."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Ищем запись для парашютиста в этой группе
        try:
            training_progress = TrainingGroupParachutist.objects.get(group=group, parachutist=parachutist)
        except TrainingGroupParachutist.DoesNotExist:
            return Response(
                {"status": "error", "message": "Запись для данного парашютиста в учебной группе не найдена."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем данные из запроса
        theory_passed = request.data.get('theory_passed', training_progress.theory_passed)
        practice_passed = request.data.get('practice_passed', training_progress.practice_passed)
        exam_passed = request.data.get('exam_passed', training_progress.exam_passed)

        # Обновляем статус парашютиста
        training_progress.theory_passed = theory_passed
        training_progress.practice_passed = practice_passed
        training_progress.exam_passed = exam_passed

        # Обновляем поле ready_for_jump в зависимости от выполнения всех чекпоинтов
        training_progress.ready_for_jump = theory_passed and practice_passed and exam_passed

        # Сохраняем изменения
        training_progress.save()

        return Response({
            "status": "ok"
        }, status=status.HTTP_200_OK)


class EndTrainingAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, instructor_id, group_id):
        # Получаем группу и проверяем, что инструктор совпадает
        group = get_object_or_404(TrainingGroup, pk=group_id, instructor_id=instructor_id)

        # Проверка, что группа в статусе "in_progress"
        if group.status != 'in_progress':
            return Response({
                "status": "error",
                "message": "Группа не в процессе, нельзя завершить обучение."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Меняем статус на "completed"
        group.status = 'completed'
        group.end_date_time = timezone.now()  # Выставляем дату завершения
        group.save()

        return Response({
            "status": "ok",
            "group_status": group.status
        }, status=status.HTTP_200_OK)


# TODO

class JumpGroupsListAPIView(APIView):
    def get(self, request, instructor_id):
        # Проверка, что инструктор существует
        instructor = get_object_or_404(Instructor, pk=instructor_id)

        # Получаем группы, где он участвует как воздушный или наземный
        jump_groups = JumpGroup.objects.filter(
            models.Q(instructor_air=instructor) | models.Q(instructor_ground=instructor)
        ).distinct()

        result = []
        for group in jump_groups:
            # Получаем заявки на прыжки для этой группы
            requests = JumpRequest.objects.filter(jump_group=group)

            # Список парашютистов
            parachutists = [
                {
                    "id": req.parachutist.parachutist_id,
                    "full_name": f"{req.parachutist.first_name} {req.parachutist.last_name}",
                    "request_status": req.request_status,
                }
                for req in requests
            ]

            group_data = {
                "jump_group_id": group.id,
                "jump_date": group.jump_date,
                "aircraft_type": group.aircraft_type,
                "altitude": group.altitude,
                "status": group.status,
                "instructor_air": {
                    "id": group.instructor_air.instructor_id,
                    "full_name": f"{group.instructor_air.first_name} {group.instructor_air.last_name}"
                },
                "instructor_ground": {
                    "id": group.instructor_ground.instructor_id,
                    "full_name": f"{group.instructor_ground.first_name} {group.instructor_ground.last_name}"
                },
                "parachutists": parachutists
            }

            result.append(group_data)

        return Response(result, status=status.HTTP_200_OK)


class StartPreJumpPreparationAPIView(APIView):
    def post(self, request, instructor_id, jump_group_id):
        # Получаем прыжковую группу
        jump_group = get_object_or_404(JumpGroup, pk=jump_group_id)

        # Получаем инструктора
        instructor = get_object_or_404(Instructor, pk=instructor_id)

        # Проверка, что инструктор может менять статус группы
        if instructor not in [jump_group.instructor_air, jump_group.instructor_ground]:
            return Response({
                "status": "error",
                "message": "Инструктор не назначен на эту группу."
            }, status=status.HTTP_403_FORBIDDEN)

        # Проверка, что статус группы — "Запланирован"
        if jump_group.status != 'Created':
            return Response({
                "status": "error",
                "message": "Группа не в статусе 'Создана', нельзя начать подготовку."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Изменяем статус на "В процессе"
        jump_group.status = 'Progress'
        jump_group.save()

        # Получаем всех парашютистов, которые подали заявку на участие в данной группе
        jump_requests = JumpRequest.objects.filter(jump_group=jump_group)

        # Создаем объект PreJumpCheck для каждого парашютиста
        for jump_request in jump_requests:
            PreJumpCheck.objects.create(
                jump_group=jump_group,
                parachutist=jump_request.parachutist,
                theory_passed=False,
                practice_passed=False,
                medical_certified=False,
                equipment_checked=False
            )

        return Response({
            "status": "ok",
            "message": f"Статус группы '{jump_group.id}' изменен на 'В процессе'. Объекты PreJumpCheck для парашютистов созданы."
        }, status=status.HTTP_200_OK)


class PreJumpCheckAPIView(APIView):
    def patch(self, request, instructor_id, jump_group_id, parachutist_id):
        # Получаем прыжковую группу
        jump_group = get_object_or_404(JumpGroup, pk=jump_group_id)

        # Получаем парашютиста
        parachutist = get_object_or_404(Parachutist, pk=parachutist_id)

        # Проверка, что инструктор может менять запись для этого парашютиста
        instructor = get_object_or_404(Instructor, pk=instructor_id)
        if instructor not in [jump_group.instructor_air, jump_group.instructor_ground]:
            return Response({
                "status": "error",
                "message": "Инструктор не назначен на эту группу."
            }, status=status.HTTP_403_FORBIDDEN)

        # Проверяем, есть ли задание на прыжок для парашютиста в этой группе
        jump_assignment = JumpAssignment.objects.filter(parachutist=parachutist, jump_group=jump_group,
                                                        completed=False).first()
        if not jump_assignment:
            return Response({
                "status": "error",
                "message": f"Парашютист {parachutist} не имеет незавершенного задания на прыжок в этой группе."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Ищем запись PreJumpCheck для данной прыжковой группы и парашютиста
        pre_jump_check, created = PreJumpCheck.objects.get_or_create(jump_group=jump_group, parachutist=parachutist)

        # Получаем данные из запроса (если они переданы)
        theory_passed = request.data.get('theory_passed', pre_jump_check.theory_passed)
        practice_passed = request.data.get('practice_passed', pre_jump_check.practice_passed)
        medical_certified = request.data.get('medical_certified', pre_jump_check.medical_certified)
        equipment_checked = request.data.get('equipment_checked', pre_jump_check.equipment_checked)

        # Обновляем запись
        pre_jump_check.theory_passed = theory_passed
        pre_jump_check.practice_passed = practice_passed
        pre_jump_check.medical_certified = medical_certified
        pre_jump_check.equipment_checked = equipment_checked
        pre_jump_check.save()
        # TODO дублируются с training_group_parachutists. Исправить. Также добавить в модель поле что есть
        #   задание на прыжок
        return Response({
            "status": "ok",
            "message": f"Проверка перед прыжком для парашютиста {parachutist} в группе {jump_group} обновлена."
        }, status=status.HTTP_200_OK)


class TrainingGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = TrainingGroup.objects.all()
    serializer_class = TrainingGroupSerializer


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
