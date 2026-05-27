from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

def default_pacs_config():
    return {
        'aeTitle': 'LIVERSEG_AI_AE',
        'port': 104,
        'ipAddress': '192.168.10.45',
        'compression': 'Lossless JPEG-LS',
        'autoRoute': True,
        'validateOnReceive': True
    }

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('radiologist', 'Radiologist'),
        ('admin', 'Hospital Admin'),
        ('researcher', 'AI Researcher'),
        ('clinician', 'Clinician'),
        ('technician', 'Imaging Technician'),
    )
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='radiologist')
    status = models.CharField(max_length=20, default='active')
    scans_reviewed = models.IntegerField(default=0)
    
    # Embedded configurations and logs
    activities = models.JSONField(default=list)
    pacs_config = models.JSONField(default=default_pacs_config)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

class Patient(models.Model):
    id = models.CharField(max_length=20, primary_key=True) # E.g., PT-2094-A
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    scan_date = models.DateTimeField(auto_now_add=True)
    modality = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Ready') # Completed, Analyzing, Ready
    has_file = models.BooleanField(default=False)
    has_lesions = models.BooleanField(default=False)
    lesion_volume = models.CharField(max_length=50, blank=True, null=True)
    findings = models.TextField(blank=True, null=True)
    signature = models.CharField(max_length=100, blank=True, null=True)

    # Metrics stored as a JSON field for simplicity
    metrics = models.JSONField(default=dict)
    slices = models.JSONField(default=list)

    def __str__(self):
        return self.name


