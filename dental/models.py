from django.db import models

from core.base_model import BaseModel
from core.models import Doctor


class DentalBraches(BaseModel):
    name = models.CharField(max_length=150, null=True)
    address = models.TextField()
    doctor = models.ForeignKey(Doctor, related_name="dental_branch_doctor", on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=11, null=True)

class DentalInfor(BaseModel):
    dental_branch = models.ForeignKey(DentalBraches, related_name="dental_branch_info", on_delete=models.CASCADE, null=True)
    fields = models.CharField(max_length=255, null=True)
    values = models.TextField(null=True)

class DentalZone(BaseModel):
    name = models.CharField(max_length=255, null=True)
    dental_branch = models.ForeignKey(DentalBraches, related_name="dental_branch_zone", on_delete=models.CASCADE)
    code = models.CharField(max_length=5, null=True)

class Room(BaseModel):
    name = models.CharField(max_length=50)
    branch = models.ForeignKey(DentalBraches, related_name="branch_room", on_delete=models.CASCADE)
