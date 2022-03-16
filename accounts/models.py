from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_number, password=None):
        if not email:
            raise ValueError('user must have E-mail')

        if not username:
            raise ValueError('user should have username')

        user = self.model(first_name=first_name, last_name=last_name, username=username,
                          email=self.normalize_email(email), phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, phone_number, email, password):
        user = self.create_user(first_name=first_name, last_name=last_name, username=username,
                                email=self.normalize_email(email), password=password, phone_number=phone_number)
        user.is_admin = True
        user.save(using=self._db)
        return user
    # Create your models here.


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=10)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class Address(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)
    address_line_1 = models.TextField()
    address_line_2 = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.IntegerField()
