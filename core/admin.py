from django.contrib import admin
from .models import User, Role, DoctorInfor

# Register your models here.
admin.site.register(Role)
admin.site.register(User)
admin.site.register(DoctorInfor)