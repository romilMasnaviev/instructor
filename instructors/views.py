from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *

class TrainingGroupViewSet(viewsets.ModelViewSet):
    queryset = TrainingGroup.objects.all()
    serializer_class = TrainingGroupSerializer

    @action(detail=True, methods=['post'])
    def parachutists(self, request, pk=None):
        group = self.get_object()
        parachutist_id = request.data.get('parachutist_id')
        try:
            parachutist = Parachutist.objects.get(pk=parachutist_id)
            TrainingGroupParachutist.objects.create(group=group, parachutist=parachutist)
            return Response(status=status.HTTP_201_CREATED)
        except Parachutist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def parachutists(self, request, pk=None, parachutist_id=None):
        group = self.get_object()
        try:
            relation = TrainingGroupParachutist.objects.get(group=group, parachutist_id=parachutist_id)
            relation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TrainingGroupParachutist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def parachutists(self, request, pk=None):
        group = self.get_object()
        relations = TrainingGroupParachutist.objects.filter(group=group)
        serializer = TrainingGroupParachutistSerializer(relations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], url_path='parachutists/(?P<parachutist_id>\d+)/progress')
    def update_progress(self, request, pk=None, parachutist_id=None):
        try:
            relation = TrainingGroupParachutist.objects.get(group_id=pk, parachutist_id=parachutist_id)
            serializer = TrainingGroupParachutistSerializer(relation, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TrainingGroupParachutist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class JumpGroupViewSet(viewsets.ModelViewSet):
    queryset = JumpGroup.objects.all()
    serializer_class = JumpGroupSerializer

    @action(detail=True, methods=['post'])
    def instructors(self, request, pk=None):
        group = self.get_object()
        instructor_id = request.data.get('instructor_id')
        role = request.data.get('role')  # 'air' or 'ground'
        try:
            instructor = Instructor.objects.get(pk=instructor_id)
            if role == 'air':
                group.instructor_air = instructor
            elif role == 'ground':
                group.instructor_ground = instructor
            group.save()
            return Response(status=status.HTTP_200_OK)
        except Instructor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def parachutists(self, request, pk=None):
        group = self.get_object()
        parachutist_id = request.data.get('parachutist_id')
        try:
            parachutist = Parachutist.objects.get(pk=parachutist_id)
            JumpRequest.objects.create(jump_group=group, parachutist=parachutist)
            return Response(status=status.HTTP_201_CREATED)
        except Parachutist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def parachutists(self, request, pk=None, parachutist_id=None):
        group = self.get_object()
        try:
            request = JumpRequest.objects.get(jump_group=group, parachutist_id=parachutist_id)
            request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except JumpRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['put'])
    def status(self, request, pk=None):
        group = self.get_object()
        serializer = JumpGroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JumpRequestViewSet(viewsets.ModelViewSet):
    queryset = JumpRequest.objects.all()
    serializer_class = JumpRequestSerializer

class PreJumpCheckViewSet(viewsets.ModelViewSet):
    queryset = PreJumpCheck.objects.all()
    serializer_class = PreJumpCheckSerializer

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        if group_id:
            return PreJumpCheck.objects.filter(jump_group_id=group_id)
        return super().get_queryset()

class JumpAssignmentViewSet(viewsets.ModelViewSet):
    queryset = JumpAssignment.objects.all()
    serializer_class = JumpAssignmentSerializer

    @action(detail=True, methods=['put'])
    def complete(self, request, pk=None):
        assignment = self.get_object()
        assignment.completed = True
        assignment.score = request.data.get('score')
        assignment.save()
        serializer = JumpAssignmentSerializer(assignment)
        return Response(serializer.data)