from rest_framework import viewsets
from .models import Parachutist
from .serializers import ParachutistSerializer

class ParachutistViewSet(viewsets.ModelViewSet):
    queryset = Parachutist.objects.all()
    serializer_class = ParachutistSerializer

