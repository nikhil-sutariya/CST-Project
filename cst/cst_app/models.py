from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email,password, **extra_fields)

''' User class is our custom User model for our users '''

class User(AbstractUser):
    ROLE_CHOICES = (
        ('Platform Admin', 'Platform Admin'),
        ('Agency Admin', 'Agency Admin'),
        ('Customer Admin', 'Customer Admin'),
        ('Agency Standard user', 'Agency Standard user'),
        ('Customer Standard User', 'Customer Standard User'),
    )

    username = None
    role = models.CharField(_('user type'), max_length= 50, choices= ROLE_CHOICES, blank=True, null=True, default='Customer Standard User')    
    email = models.EmailField(_('email address'), unique= True)
    phone = models.CharField(_('phone number'), max_length= 10,blank=True, null=True)
    is_linked = models.BooleanField(_('is linked with google or bing'), default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "Users"
        verbose_name = "Users"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

class Agency(models.Model):
    agency_name = models.CharField(_('agency name'), max_length= 50)
    agency_url = models.CharField(_('agency url'), max_length= 150, unique= True)
    address = models.CharField(_('address'), max_length= 100)
    work_phone = models.CharField(_('work phone'), max_length= 50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Agency"
        verbose_name = "Agency"
        verbose_name_plural = "Agencies"

    def __str__(self):
        return self.created_by.email

class Customer(User):
    agency_name = models.ForeignKey(Agency, related_name='Agency', on_delete=models.CASCADE)
    is_first_login = models.BooleanField(_('is fist login'), default=False)

    class Meta:
        db_table = "Customer"
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.email