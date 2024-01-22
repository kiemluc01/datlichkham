from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from datetime import datetime
from rest_framework.permissions import AllowAny, IsAuthenticated
import django_filters
from django.conf import settings
from django.db.models import Q

from django.core.mail import EmailMultiAlternatives
from django.template.loader import  render_to_string

from .models import *
from .serializers import MenuItemSerializer, MenuSerializer, BookingSerializer, NotificationSerializer, ReadBookingSerializer
from core.serializers import CustomerSerializer
from core.models import User


class MenuView(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    permission_classes = [AllowAny,]
    pagination_class = None

class MenuItemFilter(django_filters.FilterSet):
    menu = django_filters.CharFilter(field_name='menu')
class MenuItemView(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    permission_classes = [AllowAny,]
    pagination_class = None
    filterset_class = MenuItemFilter

class BookingFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status")
class BookingView(viewsets.ModelViewSet):
    serializer_class = ReadBookingSerializer
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated,]
    filterset_class = BookingFilter
    ordering = ["-created_at"]
    search_field = ["user__name", "booking_name", "user__email"]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadBookingSerializer
        return BookingSerializer

    def get_queryset(self):
        search_value = self.request.query_params.get("search", None)
        if search_value:
            search = search_value.replace(" ", ".*")
            print(search)
            return self.queryset.filter(
                Q(is_user=True, user__name__iregex=search) |
                Q(is_user=False, booking_name__iregex=search) |
                Q(is_user=True, user__email__contains=search_value)
            )
        return self.queryset

    def send_mail(self, email, time, branch, room, item, quantity):
        mail_from = settings.EMAIL_HOST_USER
        mail_to = email
        subject = "NHA KHOA THANH SƠN - THÔNG BÁO ĐẶT LỊCH"
        data = {'email': mail_from, 'mail_to':mail_to,'subject':subject}
        current_time = datetime.now()
        current_time = current_time.strftime('%H:%M:%S - %d:%m:%y')
        content = {
            "current_time":current_time,
            "email": mail_to,
            "time": time, 
            "branch": branch,
            "room": room,
            "item": item, 
            "quantity": quantity
        }
        subject, from_email, to = subject, mail_from, email
        html_content = render_to_string('mail.html',context=content)
        msg = EmailMultiAlternatives(subject, None, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def create(self, request):
        request.data["date"] = datetime.fromtimestamp(request.data["date"])
        serializer = BookingSerializer(
            data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user, status="chưa khám")
            status_no = 'new' if self.request.user.role.name == 2 else 'read'
            Notification.objects.create(booking=serializer.instance, status=status_no)
            if self.request.user.role.name == 2:
                self.send_mail(
                    self.request.user.email, 
                    serializer.instance.created_at,
                    serializer.instance.room.branch.name,
                    serializer.instance.room.name,
                    serializer.instance.item.name,
                    serializer.instance.quantity
                )
            return Response(ReadBookingSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        request.data["date"] = datetime.fromtimestamp(request.data["date"])
        return super().update(request, *args, **kwargs)

class NotificationView(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny,]
    pagination_class = None
    ordering = ['-created_at']

class RetriveNotificationView(RetrieveUpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny,]

    def update(self, request, *args, **kwargs):
        object = self.get_object()
        object.status = 'read'
        object.save()
        return Response(self.serializer_class(object).data)

class CustomerView(ListAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny,]
    queryset = User.objects.all()
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = self.queryset.filter(
            role__name=2
        )
        search = self.request.query_params.get("search", None)
        if search and search != '':
            search = search.replace(' ', '.*')
            queryset = queryset.filter(
                name__iregex=search
            )
        return queryset

class ListUserBookingView(ListAPIView):
    serializer_class = ReadBookingSerializer
    model = Booking
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]
    ordering = ["-created_at"]

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user
        )

class RetriveUpdateBookingView(RetrieveUpdateAPIView):
    serializer_class = ReadBookingSerializer
    model = Booking
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role.name == 1:
            return self.queryset
        return self.queryset.filter(
            user=self.request.user
        )

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.status = "đã huỷ"
        obj.save()
        Notification.objects.create(booking=obj, status="cancel")
        return Response(self.serializer_class(obj).data)
