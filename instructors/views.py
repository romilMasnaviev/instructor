# views.py
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

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
