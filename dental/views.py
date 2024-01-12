from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
import django_filters 
from rest_framework.response import Response

from .serializers import ReadDentalBranchesSerializer, DentalZoneSerializer, DentalInforSerializer, RoomSerializer, CreateDentalBranchesSerializer
from .models import DentalZone, DentalBraches, DentalInfor, Room


class FiterBranch(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name")
class DentalBrachView(viewsets.ModelViewSet):
    queryset = DentalBraches.objects.all()
    serializer_class = ReadDentalBranchesSerializer
    permission_classes = [AllowAny]
    filterset_class = FiterBranch

    def list(self, request):
        list_all = self.request.query_params.get("all", None)
        if list_all:
            doctor = DentalBraches.objects.all()
            return Response(self.serializer_class(doctor, many=True).data)
        return super().list(request)

    def create(self, request, *args, **kwargs):
        rooms = request.data.pop("branch_room")
        serializer = CreateDentalBranchesSerializer(
            data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            for item in rooms:
                Room.objects.create(**item, branch=serializer.instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
class FiterZone(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name")
    dental_branch = django_filters.CharFilter(field_name="dental_branch")

class DentalZoneView(viewsets.ModelViewSet):
    queryset = DentalZone.objects.all()
    serializer_class = DentalZoneSerializer
    permission_classes = [AllowAny]
    filterset_class = FiterZone

class FilterInfo(django_filters.FilterSet):
    dental_branch = django_filters.CharFilter(field_name="dental_branch")
class DentalInfoView(viewsets.ModelViewSet):
    queryset = DentalInfor.objects.all()
    serializer_class = DentalInforSerializer
    permission_classes = [AllowAny]
    filterset_class = FilterInfo

class FilterRoom(django_filters.FilterSet):
    branch = django_filters.CharFilter(field_name="branch")
class RoomView(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]
    filterset_class = FilterRoom
