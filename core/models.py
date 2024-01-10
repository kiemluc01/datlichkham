from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from .base_model import BaseModel


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{"email__iexact": username})

ROLE_CHOSE = (
    (1, "ADMIN"),
    (2, "CUSTOMER"),
    (3, "DOCTOR"),
)
class Role(BaseModel):
    name = models.IntegerField(choices=ROLE_CHOSE, default=2, unique=True)

class User(AbstractUser, BaseModel):
    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, unique=True)
    role = models.ForeignKey(Role, related_name="role", on_delete=models.CASCADE, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        db_table = u'user'


class Doctor(BaseModel):
    name = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=254, null=True)
    position = models.CharField(max_length=150, null=True)
    DoB = models.DateTimeField(null=True)
    degree_infor = models.TextField(null=True)

class DoctorDetail(BaseModel):
    doctor = models.ForeignKey("core.Doctor", related_name="doctor_detail", on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
