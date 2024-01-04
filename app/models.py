from django.db import models

from core.base_model import BaseModel


class Menu(BaseModel):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

class MenuItem(BaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    menu = models.ForeignKey("app.Menu", related_name="items", on_delete=models.CASCADE)

class Booking(BaseModel):
    user = models.ForeignKey("core.User", related_name="user_booking", on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    quantity = models.IntegerField(default=1)
    total_money = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
    status = models.CharField(max_length=150, blank=True, default="booking")
    reason = models.CharField(max_length=255)
    doctor = models.ForeignKey("core.Doctor", related_name="doctor_booking", on_delete=models.CASCADE, null=True)

class Notification(BaseModel):
    booking = models.ForeignKey("app.Booking", related_name="booking_notificate", on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='new')
