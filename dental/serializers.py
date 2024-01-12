from rest_framework import serializers

from .models import *
from core.serializers import DoctorSerializer


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
class ReadDentalBranchesSerializer(serializers.ModelSerializer):
    branch_room = RoomSerializer(many=True, read_only=True)
    doctor = DoctorSerializer(read_only=True)
    class Meta:
        model = DentalBraches
        fields = '__all__'

class CreateDentalBranchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DentalBraches
        fields = '__all__'
class DetailRoomSerializer(serializers.ModelSerializer):
    branch = CreateDentalBranchesSerializer(read_only=True)
    class Meta:
        model = Room
        fields = '__all__'

class DentalZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DentalZone
        fields = '__all__'
        extra_kwargs = {
            "user": {"read_only": True},
        }

class DentalInforSerializer(serializers.ModelSerializer):
    class Meta:
        model = DentalInfor
        fields = '__all__'