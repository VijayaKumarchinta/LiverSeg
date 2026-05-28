from rest_framework import serializers
from .models import User, Patient
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

    def to_representation(self, instance):

        data = super().to_representation(instance)

        request = self.context.get('request')

        if request:

            # Non-admins should not see PACS internals
            if request.user.role != 'admin':
                data.pop('pacs_config', None)

            # Hide activity audit trail from non-admins
            if request.user.role != 'admin':
                data.pop('activities', None)

        return data
class PatientSerializer(serializers.ModelSerializer):
    # Return absolute URLs for file fields so the frontend can use them directly
    ct_scan_url = serializers.SerializerMethodField()
    liver_mask_url = serializers.SerializerMethodField()
    preview_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = '__all__'

    def get_ct_scan_url(self, obj):

        if obj.ct_scan:

            request = self.context.get('request')

            if request:
                return request.build_absolute_uri(
                    f"/media/{obj.ct_scan.name}"
                )

        return None

    def get_liver_mask_url(self, obj):

        if obj.liver_mask:

            request = self.context.get('request')

            if request:
                return request.build_absolute_uri(
                    f"/media/{obj.liver_mask.name}"
                )

        return None
        
    def get_preview_image_url(self, obj):
        if obj.preview_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.preview_image.url)
            return obj.preview_image.url
        return None
