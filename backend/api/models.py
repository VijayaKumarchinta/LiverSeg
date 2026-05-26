from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLE_CHOICES = (
        ('radiologist', 'Radiologist'),
        ('admin', 'Hospital Admin'),
        ('researcher', 'AI Researcher'),
        ('clinician', 'Clinician'),
        ('technician', 'Imaging Technician'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='radiologist')
    department = models.CharField(max_length=100, default='Radiology')
    hospital = models.CharField(max_length=100, default='St. Luke Medical Center')
    status = models.CharField(max_length=20, default='active')
    scans_reviewed = models.IntegerField(default=0)

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

    def __str__(self):
        return self.name

class Slice(models.Model):
    patient = models.ForeignKey(Patient, related_name='slices', on_delete=models.CASCADE)
    slice_index = models.IntegerField()
    liver_size = models.FloatField(default=0)
    liver_x = models.FloatField(default=0)
    liver_y = models.FloatField(default=0)
    lesion_size = models.FloatField(default=0)
    lesion_x = models.FloatField(default=0)
    lesion_y = models.FloatField(default=0)

    def __str__(self):
        return f"Slice {self.slice_index} for {self.patient.id}"

class ActivityLog(models.Model):
    action = models.CharField(max_length=100)
    details = models.CharField(max_length=255)
    time = models.CharField(max_length=50) # Could be DateTime, but string for mock parity
    type = models.CharField(max_length=20, default='info') # info, success

    def __str__(self):
        return self.action

class PacsConfig(models.Model):
    ae_title = models.CharField(max_length=50, default='LIVERSEG_AI_AE')
    port = models.IntegerField(default=104)
    ip_address = models.CharField(max_length=50, default='192.168.10.45')
    auto_route = models.BooleanField(default=True)
    validate_on_receive = models.BooleanField(default=True)
    compression = models.CharField(max_length=50, default='Lossless JPEG-LS')

    def __str__(self):
        return self.ae_title

class AuditLog(models.Model):
    user = models.CharField(max_length=100) # Storing name for simplicity instead of FK
    action = models.CharField(max_length=100)
    resource = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action}"
