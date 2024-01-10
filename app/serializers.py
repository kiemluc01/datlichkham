from rest_framework import serializers

from .models import *
from core.serializers import ProfileSerializer


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()

    # def validate(self, data):
        
    class Meta:
        model = Booking
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
        }

class NotificationSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    def get_name(self, object):
        if not object.booking.is_user:
            return object.booking.booking_name
        if object.booking.user.name in [None, '']:
            return object.booking.user.email
        return object.booking.user.name
    class Meta:
        model = Notification
        fields = '__all__'
