from rest_framework import serializers
from .models import User, Role, DoctorInfor


# class serializer dùng để validate data và show data
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User 
        fields = ["id", "name", "phone", "email", "role", "created_at", "updated_at"]
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

class DoctorInforSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorInfor
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

class ProfileSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    doctor_infor = DoctorInforSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ["id", "name", "phone", "email", "created_at", "updated_at"]
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }