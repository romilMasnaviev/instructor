from rest_framework import serializers
from .models import Parachutist

class ParachutistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parachutist
        fields = '__all__'

