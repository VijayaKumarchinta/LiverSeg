from rest_framework import serializers
from .models import User, Patient, Slice, ActivityLog, PacsConfig, AuditLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'department', 'hospital', 'status', 'scans_reviewed')

class SliceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slice
        fields = ('slice_index', 'liver_size', 'liver_x', 'liver_y', 'lesion_size', 'lesion_x', 'lesion_y')

class PatientSerializer(serializers.ModelSerializer):
    slices = SliceSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = '__all__'

class PacsConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacsConfig
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
