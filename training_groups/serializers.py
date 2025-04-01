from rest_framework import serializers
from .models import TrainingGroup
from parachutists.serializers import ParachutistSerializer

class TrainingGroupSerializer(serializers.ModelSerializer):
    parachutists = ParachutistSerializer(many=True, read_only=True)

    class Meta:
        model = TrainingGroup
        fields = '__all__'

