from django.db import models
from django.contrib.auth.models import AbstractUser
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

class User(AbstractUser):
    ROLE_CHOICES = (
        ('radiologist', 'Radiologist'),
        ('admin', 'Hospital Admin'),
        ('researcher', 'AI Researcher'),
        ('clinician', 'Clinician'),
        ('technician', 'Imaging Technician'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='radiologist')
    status = models.CharField(max_length=20, default='active')
    scans_reviewed = models.IntegerField(default=0)
    
    # Embedded configurations and logs
    activities = models.JSONField(default=list)
    pacs_config = models.JSONField(default=default_pacs_config)

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
    has_lesions = models.BooleanField(default=False)
    lesion_volume = models.CharField(max_length=50, blank=True, null=True)
    findings = models.TextField(blank=True, null=True)
    signature = models.CharField(max_length=100, blank=True, null=True)

    # Metrics stored as a JSON field for simplicity
    metrics = models.JSONField(default=dict)
    slices = models.JSONField(default=list)

    def __str__(self):
        return self.name


