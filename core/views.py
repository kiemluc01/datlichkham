from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime
import base64

from .services import getResponseGPTFromText
from .serializers import RegisterSerializer, ProfileSerializer, RoleSerializer, DoctorSerializer, GPTSerializer, UpdateProfileSerializer
from .models import User, Doctor, Role, DoctorDetail


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
                name=serializer.validated_data.get("name"),
                role=role,
                is_staff=True,
            )
            return Response(ProfileSerializer(user).data, status=status.HTTP_201_CREATED)
class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated,]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        return Response(self.serializer_class(user).data)
    
    def put(self, request):
        user = request.user
        serializer = UpdateProfileSerializer(user, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class RoleView(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    permission_classes = [AllowAny]

class DoctorView(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    permission_classes = [AllowAny]
    
    def list(self, request):
        list_all = self.request.query_params.get("all", None)
        if list_all:
            doctor = Doctor.objects.all()
            return Response(DoctorSerializer(doctor, many=True).data)
        return super().list(request)

    def create(self, request, *args, **kwargs):
        images=[]
        if "images[]" in request.data:
            images = request.data.pop("images[]")
        request.data['DoB'] = datetime.fromtimestamp(int(request.data['DoB']))
        serializer = self.serializer_class(
            data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            for image in images:
                DoctorDetail.objects.create(
                    doctor=serializer.instance,
                    image=image
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        images=[]
        object = self.get_object()
        if "images[]" in request.data:
            images = request.data.pop("images[]")
        request.data['DoB'] = datetime.fromtimestamp(int(request.data['DoB']))
        serializer = self.serializer_class(
            instance=object,data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            DoctorDetail.objects.filter(doctor=serializer.instance).delete()
            for image in images:
                DoctorDetail.objects.create(
                    doctor=serializer.instance,
                    image=image
                )
            return Response(serializer.data, status=status.HTTP_200_OK)


class GetPostFromGPTAPIView(GenericAPIView):
    serializer_class = GPTSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            response = getResponseGPTFromText(user_input=str(serializer.validated_data.get("user_input")))
            return Response({"data": response})
