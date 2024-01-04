from rest_framework import serializers
from .models import User, Role, Doctor, DoctorDetail


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

class DoctorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorDetail
        fields = '__all__'
class DoctorSerializer(serializers.ModelSerializer):
    doctor_detail = DoctorDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Doctor
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

class ProfileSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ["id", "name", "phone", "email", "role","created_at", "updated_at"]
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    name = serializers.CharField(required=False)
    phone = serializers.CharField()
    class Meta:
        model = User
        fields = ["id", "email", "name", "phone", "password"]

    def validate(self, data):
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Email is already exists!")
        return data

class GPTSerializer(serializers.Serializer):
    user_input = serializers.CharField()
