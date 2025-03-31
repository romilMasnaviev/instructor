from rest_framework import serializers
from .models import *


class ParachutistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parachutist
        fields = '__all__'


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = '__all__'


class TrainingGroupSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    instructor_id = serializers.PrimaryKeyRelatedField(
        queryset=Instructor.objects.all(), source='instructor', write_only=True
    )

    class Meta:
        model = TrainingGroup
        fields = '__all__'


class TrainingGroupParachutistSerializer(serializers.ModelSerializer):
    parachutist = ParachutistSerializer(read_only=True)
    group = TrainingGroupSerializer(read_only=True)

    class Meta:
        model = TrainingGroupParachutist
        fields = '__all__'


class JumpGroupSerializer(serializers.ModelSerializer):
    instructor_air = InstructorSerializer(read_only=True)
    instructor_ground = InstructorSerializer(read_only=True)

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