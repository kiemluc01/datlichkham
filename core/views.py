from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .services import getResponseGPTFromText
from .serializers import RegisterSerializer, ProfileSerializer, RoleSerializer, DoctorSerializer, GPTSerializer
from .models import User, Doctor, Role


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            role = Role.objects.get(name=2)
            user = User.objects.create_user(
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
                phone=serializer.validated_data.get("phone"),
                role=role,
                is_staff=True,
            )
            return Response(ProfileSerializer(user).data, status=status.HTTP_201_CREATED)
class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        return Response(self.serializer_class(user).data)


class RoleView(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    # permission_classes = [IsAuthenticated]

class DoctorView(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()


class GetPostFromGPTAPIView(GenericAPIView):
    serializer_class = GPTSerializer
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            response = getResponseGPTFromText(user_input=str(serializer.validated_data.get("user_input")))
            return Response({"data": response})
