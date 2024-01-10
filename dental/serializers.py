from rest_framework import serializers

from .models import *


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
class DentalBranchesSerializer(serializers.ModelSerializer):
    branch_room = RoomSerializer(many=True, read_only=True)
    class Meta:
        model = DentalBraches
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