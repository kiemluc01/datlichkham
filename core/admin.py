from django.contrib import admin
from .models import User, Role, Doctor, DoctorDetail

# Register your models here.
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(DoctorDetail)