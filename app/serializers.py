from rest_framework import serializers

from .models import *
from core.serializers import ProfileSerializer
from dental.serializers import DetailRoomSerializer


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"

class ReadMenuItemSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = "__all__"

class ReadBookingSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    room = DetailRoomSerializer(read_only=True)
    item = ReadMenuItemSerializer(read_only=True)
    total_money = serializers.SerializerMethodField(read_only=True)
    
    def get_total_money(self, obj):
        return obj.incurred + obj.item.price * obj.quantity
    class Meta:
        model = Booking
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
            "total_money": {"read_only": True},
        }

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
            "total_money": {"read_only": True},
        }

class NotificationSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    booking = BookingSerializer(read_only=True)
    
    def get_name(self, object):
        if not object.booking.is_user:
            return object.booking.booking_name
        if object.booking.user.name in [None, '']:
            return object.booking.user.email
        return object.booking.user.name
    class Meta:
        model = Notification
        fields = '__all__'
