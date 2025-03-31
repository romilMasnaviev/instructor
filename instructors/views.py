# instructors/views.py
from rest_framework import viewsets
from .models import (
    Parachutist,
    Instructor,
    TrainingGroup,
    TrainingGroupParachutist,
    JumpGroup,
    JumpRequest,
    JumpAssignment,
    PreJumpCheck,
)
from .serializers import (
    ParachutistSerializer,
    InstructorSerializer,
    TrainingGroupSerializer,
    TrainingGroupParachutistSerializer,
    JumpGroupSerializer,
    JumpRequestSerializer,
    JumpAssignmentSerializer,
    PreJumpCheckSerializer,
)

class ParachutistViewSet(viewsets.ModelViewSet):
    queryset = Parachutist.objects.all()
    serializer_class = ParachutistSerializer

class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

class TrainingGroupViewSet(viewsets.ModelViewSet):
    queryset = TrainingGroup.objects.all()
    serializer_class = TrainingGroupSerializer

class TrainingGroupParachutistViewSet(viewsets.ModelViewSet):
    queryset = TrainingGroupParachutist.objects.all()
    serializer_class = TrainingGroupParachutistSerializer

class JumpGroupViewSet(viewsets.ModelViewSet):
    queryset = JumpGroup.objects.all()
    serializer_class = JumpGroupSerializer

class JumpRequestViewSet(viewsets.ModelViewSet):
    queryset = JumpRequest.objects.all()
    serializer_class = JumpRequestSerializer

class JumpAssignmentViewSet(viewsets.ModelViewSet):
    queryset = JumpAssignment.objects.all()
    serializer_class = JumpAssignmentSerializer

class PreJumpCheckViewSet(viewsets.ModelViewSet):
    queryset = PreJumpCheck.objects.all()
    serializer_class = PreJumpCheckSerializer
