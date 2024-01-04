"""
URL configuration for datlichkham project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from core.views import RegisterAPIView, GetPostFromGPTAPIView, RoleView, ProfileView
from post.views import PostView, CategoryView
from app.views import BookingView, NotificationView, RetriveNotificationView
from dental.views import DentalBrachView, DentalInfoView, DentalZoneView
router = DefaultRouter()
##### Role #####
router.register('api/core/roles', RoleView, basename="roles"),
##### Role #####

##### Post #####
router.register('api/post/categories', CategoryView, basename="categories"),
router.register('api/post/posts', PostView, basename="posts"),
##### Post #####

##### app #####
router.register('api/app/bookings', BookingView, basename="bookings"),
##### app #####

##### dental #####
router.register('api/dental/branches', DentalBrachView, basename="branches"),
router.register('api/dental/infor', DentalInfoView, basename="info"),
router.register('api/dental/zones', DentalZoneView, basename="zones"),
##### dental #####

urlpatterns =router.urls +[
    path('admin/', admin.site.urls),
    
    ########### core urls ##########
    
    ##### auth #####
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/register/', RegisterAPIView.as_view(), name="register"),
    ##### auth #####
    
    ##### GPT #####
    path('api/openAI/GPT/get-response-by-text', GetPostFromGPTAPIView.as_view(), name='GPT_openai'),
    ##### GPT #####
    
    ##### Profile #####
    path('api/users/me', ProfileView.as_view(), name='profile'),
    ##### Profile #####
    
    path('api/app/notifications', NotificationView.as_view(), name='notifications'),
    path('api/app/notifications/<str:pk>', RetriveNotificationView.as_view(), name='notification_update'),
    
    ########### core urls ##########
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)