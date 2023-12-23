from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .services import getResponseGPTFromText
from .serializers import RegisterSerializer, ProfileSerializer, RoleSerializer, DoctorInforSerializer, GPTSerializer
from .models import User, DoctorInfor, Role


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(role_id=2)
            DoctorInfor.objects.create(user=serializer.instance)
            return Response(ProfileSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
class ProfileView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        return Response(self.serializer_class(user).data)


class RoleView(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    # permission_classes = [IsAuthenticated]

class DoctorInforView(viewsets.ModelViewSet):
    serializer_class = DoctorInforSerializer
    queryset = DoctorInfor.objects.all()


class GetPostFromGPTAPIView(GenericAPIView):
    serializer_class = GPTSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            response = getResponseGPTFromText(user_input=str(serializer.validated_data.get("user_input")))
            return Response({"data": response})
