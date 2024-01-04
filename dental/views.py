from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
import django_filters 

from .serializers import DentalBranchesSerializer, DentalZoneSerializer, DentalInforSerializer
from .models import DentalZone, DentalBraches, DentalInfor


class FiterBranch(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name")
class DentalBrachView(viewsets.ModelViewSet):
    queryset = DentalBraches.objects.all()
    serializer_class = DentalBranchesSerializer
    permission_classes = [AllowAny]
    filterset_class = FiterBranch

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
