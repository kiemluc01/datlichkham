from rest_framework import serializers

from .models import *


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
        }

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
