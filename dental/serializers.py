from rest_framework import serializers

from .models import *


class DentalBranchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DentalBraches
        fields = '__all__'

class DentalZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DentalZone
        fields = '__all__'

class DentalInforSerializer(serializers.ModelSerializer):
    class Meta:
        model = DentalInfor
        fields = '__all__'