from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import TrainingGroup, JumpGroup, Parachutist, TrainingGroupParachutist, JumpRequest, PreJumpCheck, JumpAssignment
from .serializers import TrainingGroupSerializer, JumpGroupSerializer, ParachutistSerializer, JumpRequestSerializer, PreJumpCheckSerializer, JumpAssignmentSerializer


class TrainingGroupViewSet(viewsets.ModelViewSet):
    queryset = TrainingGroup.objects.all()
    serializer_class = TrainingGroupSerializer

    @action(detail=True, methods=['get'], url_path='parachutists')
    def get_parachutists(self, request, pk=None):
        group = self.get_object()
        parachutists = group.traininggroupparachutist_set.select_related('parachutist')
        serializer = ParachutistSerializer([tp.parachutist for tp in parachutists], many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='parachutists')
    def add_parachutist(self, request, pk=None):
        group = self.get_object()
        parachutist_id = request.data.get('parachutist_id')
        parachutist = get_object_or_404(Parachutist, pk=parachutist_id)
        TrainingGroupParachutist.objects.get_or_create(parachutist=parachutist, group=group)
        return Response({'message': 'Parachutist added'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path='parachutists/(?P<parachutist_id>[^/.]+)')
    def remove_parachutist(self, request, pk=None, parachutist_id=None):
        group = self.get_object()
        parachutist = get_object_or_404(Parachutist, pk=parachutist_id)
        TrainingGroupParachutist.objects.filter(parachutist=parachutist, group=group).delete()
        return Response({'message': 'Parachutist removed'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put'], url_path='parachutists/(?P<parachutist_id>[^/.]+)/progress')
    def update_progress(self, request, pk=None, parachutist_id=None):
        parachutist_group = get_object_or_404(TrainingGroupParachutist, group_id=pk, parachutist_id=parachutist_id)
        parachutist_group.theory_passed = request.data.get('theory_passed', parachutist_group.theory_passed)
        parachutist_group.practice_passed = request.data.get('practice_passed', parachutist_group.practice_passed)
        parachutist_group.save()
        return Response({'message': 'Progress updated'})

class JumpGroupViewSet(viewsets.ModelViewSet):
    queryset = JumpGroup.objects.all()
    serializer_class = JumpGroupSerializer

    @action(detail=True, methods=['post'], url_path='status')
    def update_status(self, request, pk=None):
        group = self.get_object()
        status_value = request.data.get('status')
        if status_value not in dict(JumpGroup._meta.get_field('status').choices):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        group.status = status_value
        group.save()
        return Response({'message': 'Status updated'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='parachutists')
    def add_parachutist_to_jump_group(self, request, pk=None):
        group = self.get_object()
        parachutist_id = request.data.get('parachutist_id')
        parachutist = get_object_or_404(Parachutist, pk=parachutist_id)
        group.parachutists.add(parachutist)
        return Response({'message': 'Parachutist added to jump group'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path='parachutists/(?P<parachutist_id>[^/.]+)')
    def remove_parachutist_from_jump_group(self, request, pk=None, parachutist_id=None):
        group = self.get_object()
        parachutist = get_object_or_404(Parachutist, pk=parachutist_id)
        group.parachutists.remove(parachutist)
        return Response({'message': 'Parachutist removed from jump group'}, status=status.HTTP_204_NO_CONTENT)

class JumpRequestViewSet(viewsets.ModelViewSet):
    queryset = JumpRequest.objects.all()
    serializer_class = JumpRequestSerializer

    @action(detail=True, methods=['put'], url_path='status')
    def update_status(self, request, pk=None):
        jump_request = self.get_object()
        status_value = request.data.get('request_status')
        if status_value not in dict(JumpRequest._meta.get_field('request_status').choices):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        jump_request.request_status = status_value
        jump_request.save()
        return Response({'message': 'Status updated'}, status=status.HTTP_200_OK)

class PreJumpCheckViewSet(viewsets.ModelViewSet):
    queryset = PreJumpCheck.objects.all()
    serializer_class = PreJumpCheckSerializer

    @action(detail=True, methods=['get'], url_path='results')
    def get_results(self, request, pk=None):
        jump_group = self.get_object()
        pre_jump_check = get_object_or_404(PreJumpCheck, jump_group=jump_group)
        serializer = PreJumpCheckSerializer(pre_jump_check)
        return Response(serializer.data)

class JumpAssignmentViewSet(viewsets.ModelViewSet):
    queryset = JumpAssignment.objects.all()
    serializer_class = JumpAssignmentSerializer

    @action(detail=True, methods=['put'], url_path='complete')
    def complete_assignment(self, request, pk=None):
        assignment = self.get_object()
        assignment.completed = True
        assignment.save()
        return Response({'message': 'Jump completed'})

    @action(detail=True, methods=['put'], url_path='status')
    def update_status(self, request, pk=None):
        assignment = self.get_object()
        status_value = request.data.get('status')
        if status_value not in dict(JumpAssignment._meta.get_field('status').choices):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        assignment.status = status_value
        assignment.save()
        return Response({'message': 'Status updated'}, status=status.HTTP_200_OK)
