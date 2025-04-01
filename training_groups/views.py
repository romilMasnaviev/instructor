from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TrainingGroup
from parachutists.models import Parachutist
from .serializers import TrainingGroupSerializer

class TrainingGroupViewSet(viewsets.ModelViewSet):
    queryset = TrainingGroup.objects.all()
    serializer_class = TrainingGroupSerializer

    @action(detail=True, methods=['post'])
    def add_parachutist(self, request, pk=None):
        group = self.get_object()
        parachutist_id = request.data.get('parachutist_id')
        if parachutist_id:
            try:
                parachutist = Parachutist.objects.get(id=parachutist_id)
                group.parachutists.add(parachutist)
                return Response({'status': 'Парашютист добавлен'})
            except Parachutist.DoesNotExist:
                return Response({'error': 'Парашютист не найден'}, status=404)
        return Response({'error': 'Не указан ID парашютиста'}, status=400)

    @action(detail=True, methods=['post'])
    def remove_parachutist(self, request, pk=None):
        group = self.get_object()
        parachutist_id = request.data.get('parachutist_id')
        if parachutist_id:
            try:
                parachutist = Parachutist.objects.get(id=parachutist_id)
                group.parachutists.remove(parachutist)
                return Response({'status': 'Парашютист удален'})
            except Parachutist.DoesNotExist:
                return Response({'error': 'Парашютист не найден'}, status=404)
        return Response({'error': 'Не указан ID парашютиста'}, status=400)

    @action(detail=True, methods=['post'])
    def close_group(self, request, pk=None):
        group = self.get_object()
        group.status = 'closed'
        group.save()
        return Response({'status': 'Группа закрыта'})

