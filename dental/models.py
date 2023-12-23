from django.db import models

from core.base_model import BaseModel
from core.models import User


# Create your models here.
class DentalBraches(BaseModel):
    name = models.CharField(max_length=150, null=True)
    address = models.TextField()
    user = models.ForeignKey(User, related_name="dental_branch_user", on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, null=True)

class DentalInfor(BaseModel):
    fields = models.CharField(max_length=255, null=True)
    values = models.TextField(null=True)

class DentalZone(BaseModel):
    name = models.CharField(max_length=255, null=True)
    dental_branch = models.ForeignKey(DentalBraches, related_name="dental_branch_zone", on_delete=models.CASCADE)
    code = models.CharField(max_length=5, null=True)
