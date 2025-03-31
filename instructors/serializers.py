# instructors/serializers.py
from rest_framework import serializers
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

class ParachutistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parachutist
        fields = '__all__'

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = '__all__'

class TrainingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingGroup
        fields = '__all__'

class TrainingGroupParachutistSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingGroupParachutist
        fields = '__all__'

class JumpGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = JumpGroup
        fields = '__all__'

class JumpRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JumpRequest
        fields = '__all__'

class JumpAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JumpAssignment
        fields = '__all__'

class PreJumpCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreJumpCheck
        fields = '__all__'
