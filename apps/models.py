from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, ForeignKey, SET_NULL, TextField, TextChoices, \
    ImageField, DateTimeField,DecimalField


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone_number, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        email = self.normalize_email(email)

        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, email, password, **extra_fields)


class User(AbstractUser):
    phone_number = CharField(max_length=20, unique=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
    email=None
    username = None
    first_name = None
    last_name = None
    full_name=CharField(max_length=255)

class Category(Model):
    class TypeChoices(TextChoices):
        income='income',"Income"
        expense='expense',"Expense"

    name = CharField(max_length=50, unique=True)
    icon=ImageField(upload_to='media/category/icons', null=True, blank=True)
    type=CharField(max_length=50, choices=TypeChoices.choices)

class Expense(Model):
    class TypeChoices(TextChoices):
        income='income',"Income"
        expense='expense',"Expense"
    amount=DecimalField(max_digits=10, decimal_places=2)
    type = CharField(max_length=50, choices=TypeChoices.choices)
    description = TextField()
    category=ForeignKey(Category, on_delete=SET_NULL, null=True, blank=True)
    created_at=DateTimeField(auto_now_add=True)
    user=ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
