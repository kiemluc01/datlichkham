from django.db import models

from core.base_model import BaseModel
from dental.models import Room


class Menu(BaseModel):
    name = models.CharField(max_length=255)

class MenuItem(BaseModel):
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    menu = models.ForeignKey("app.Menu", related_name="items", on_delete=models.CASCADE)

class Booking(BaseModel):
    user = models.ForeignKey("core.User", related_name="user_booking", on_delete=models.CASCADE, null=True)
    is_user = models.BooleanField(default=True)
    booking_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateTimeField(null=True)
    quantity = models.IntegerField(default=1)
    item = models.ForeignKey("app.MenuItem", related_name="booking_item", on_delete=models.CASCADE, null=True)
    incurred = models.IntegerField(default=0, blank=True)
    total_money = models.IntegerField(default=0, blank=True)
    status = models.CharField(max_length=150, blank=True, default="chưa khám")
    reason = models.CharField(max_length=255)
    room = models.ForeignKey(Room, related_name="room_booking", on_delete=models.CASCADE, null=True)

class Notification(BaseModel):
    booking = models.ForeignKey("app.Booking", related_name="booking_notificate", on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='new')
