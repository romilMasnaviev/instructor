# serializers.py
from rest_framework import serializers
from .models import Instructor
from accounts.models import Account


class InstructorSerializer(serializers.ModelSerializer):
    # Включим в сериализатор имя инструктора (связь с Account)
    name = serializers.CharField(source='account.get_full_name')

    class Meta:
        model = Instructor
        fields = ['instructor_id', 'name', 'qualification', 'status']
