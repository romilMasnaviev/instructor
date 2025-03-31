from rest_framework import viewsets
from rest_framework import permissions
from .models import TrainingGroup, JumpGroup, JumpRequest, PreJumpCheck, JumpAssignment, TrainingGroupParachutist, Parachutist, Instructor
from .serializers import TrainingGroupSerializer, JumpGroupSerializer, JumpRequestSerializer, PreJumpCheckSerializer, JumpAssignmentSerializer, TrainingGroupParachutistSerializer, ParachutistSerializer, InstructorSerializer


# 1. TrainingGroupViewSet для учебных групп
class TrainingGroupViewSet(viewsets.ModelViewSet):
    queryset = TrainingGroup.objects.all()
    serializer_class = TrainingGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# 2. JumpGroupViewSet для прыжковых групп
class JumpGroupViewSet(viewsets.ModelViewSet):
    queryset = JumpGroup.objects.all()
    serializer_class = JumpGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# 3. JumpRequestViewSet для заявок на прыжок
class JumpRequestViewSet(viewsets.ModelViewSet):
    queryset = JumpRequest.objects.all()
    serializer_class = JumpRequestSerializer
    permission_classes = [permissions.IsAuthenticated]


# 4. PreJumpCheckViewSet для проверок перед прыжком
class PreJumpCheckViewSet(viewsets.ModelViewSet):
    queryset = PreJumpCheck.objects.all()
    serializer_class = PreJumpCheckSerializer
    permission_classes = [permissions.IsAuthenticated]


# 5. JumpAssignmentViewSet для заданий
class JumpAssignmentViewSet(viewsets.ModelViewSet):
    queryset = JumpAssignment.objects.all()
    serializer_class = JumpAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]


# 6. TrainingProgressViewSet для отслеживания обучения
class TrainingProgressViewSet(viewsets.ModelViewSet):
    queryset = TrainingGroupParachutist.objects.all()
    serializer_class = TrainingGroupParachutistSerializer
    permission_classes = [permissions.IsAuthenticated]


# 7. ParachutistViewSet для парашютистов
class ParachutistViewSet(viewsets.ModelViewSet):
    queryset = Parachutist.objects.all()
    serializer_class = ParachutistSerializer
    permission_classes = [permissions.IsAuthenticated]


# 8. InstructorViewSet для инструкторов
class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [permissions.IsAuthenticated]
