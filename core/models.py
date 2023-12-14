from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .base_model import BaseModel

# Create your models here.


class Role(BaseModel):
    name = models.CharField(max_length=150)

class User(AbstractBaseUser, BaseModel):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=11, null=True)
    email = models.EmailField(max_length=254, null=True, unique=True)
    role = models.ForeignKey(Role, related_name="role", on_delete=models.CASCADE)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class DoctorInfor(BaseModel):
    user = models.OneToOneField(User, related_name="doctor_infor" , on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    degree_infor = models.TextField(null=True)
