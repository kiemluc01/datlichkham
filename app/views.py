from rest_framework import viewsets,status
from rest_framework.response import Response
from datetime import datetime

from .models import *
from .serializers import MenuItemSerializer, MenuSerializer, BookingSerializer


class MenuView(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    permission_classes = []

class MenuItemView(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    permission_classes = []

class BookingView(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = []

    def create(self, request):
        print(request.data["date"])
        request.data["date"] = datetime.strptime(request.data["date"], '%a, %d %b %Y %H:%M:%S GMT')
        serializer = self.serializer_class(
            data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, status="booking")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
